from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Text
from control_block_diagram.predefined_components import DqToAlphaBetaTransformation, Converter, PMSM,\
    AbcToAlphaBetaTransformation, AlphaBetaToDqTransformation, Add, PIController, Multiply, DcShuntMotor, DcSeriesMotor,\
    DcConverter


def omega_stage(start, idx):
    space = 1 if idx == 0 else 1.5
    add_omega = Add(start.add_x(space))
    if idx == 0:
        Connection.connect(start, add_omega.input_left[0], text=r'$\omega_{ref}$', text_align='left',
                           text_position='start')
    pi_omega = PIController(add_omega.position.add_x(1.5), text='Speed\nController')
    Connection.connect(add_omega.output_right, pi_omega.input_left)

    inputs = dict(omega_ref=[add_omega.input_left[0], dict(text=r'$\omega_{ref}$')], omega=[add_omega.input_bottom[0],
                                        dict(text=r'-', move_text=(-0.2, -0.2), text_position='end', text_align='right')])
    outputs = dict(t_ref=pi_omega.output_right[0])
    connect_to_lines = dict()
    start = pi_omega.position

    return start, inputs, outputs, connect_to_lines


def torque_stage(start, idx):
    space = 1 if idx == 0 else 2.2
    box_torque = Box(start.add_x(space), size=(0.8, 0.8), text=r"$\frac{1}{\Psi'_{E}}$")
    if idx == 0:
        Connection.connect(start, box_torque.input_left[0], text=r'$T_{ref}$', text_align='left',
                           text_position='start')

    inputs = dict(t_ref=[box_torque.input_left[0], dict(text=r'$T^{*}$')])
    outputs = dict(i_ref=box_torque.output_right[0])
    connect_to_lines = dict()

    start = box_torque.position

    return start, inputs, outputs, connect_to_lines


def current_stage(emf_feedforward, env_id):
    def _current_stage(start, idx):
        control_task = env_id.split('-')[1]
        space = 1 if idx == 0 else 1.5
        add_current = Add(start.add_x(space))
        if idx == 0:
            Connection.connect(start, add_current.input_left[0], text=r'$i_{ref}$', text_align='left',
                               text_position='start')
        pi_current = PIController(add_current.position.add_x(1.5), text='Current\nController')
        Connection.connect(add_current.output_right, pi_current.input_left)

        inputs = dict(i_ref=[add_current.input_left[0], dict(text=r'$i^{*}$')], i=[add_current.input_bottom[0],
                        dict(text=r'-', move_text=(-0.2, -0.2), text_position='end', text_align='right')])
        outputs = dict(u=pi_current.output_right[0])
        connect_to_lines = dict()
        start = pi_current.position

        if emf_feedforward:
            add_emf = Add(pi_current.position.add_x(2))
            Connection.connect(pi_current.output_right, add_emf.input_left, text=r'$\Delta u^{*}$')

            box_psi = Box(add_emf.position.sub_y(2.5), size=(0.7, 0.7), text=r"$\Psi'_{E}$", inputs=dict(bottom=1),
                          outputs=dict(top=1))
            Connection.connect(box_psi.output_top, add_emf.input_bottom, text=r'$u^{0}$', text_position='end',
                               text_align='right', move_text=(-0.1, -0.2))
            if control_task in ['SC']:
                connect_to_lines['omega'] = [box_psi.input_bottom[0], dict(section=0)]
            elif control_task in ['CC', 'TC']:
                inputs['omega'] = [box_psi.input_bottom[0], dict()]
            outputs['u'] = add_emf.output_right[0]
            start = add_emf.position

        return start, inputs, outputs, connect_to_lines

    return _current_stage


def series_dc_stage(emf_feedforward, env_id):
    def _series_dc_stage(start, idx):
        control_task = env_id.split('-')[1]
        space = 1.5 if emf_feedforward else 2
        pwm = Box(start.add_x(space), size=(1, 0.8), text='PWM')
        converter = DcConverter(pwm.position.add_x(2), size=1.2, input_number=1)
        Connection.connect(pwm.output_right, converter.input_left, text='$S$')

        dc_shunt = DcSeriesMotor(converter.position.sub_y(3), size=1.2, input='top', output='left')

        conv_motor = Connection.connect(converter.output_bottom, dc_shunt.input_top, text=['', r'$i$'],
                                        text_align='right', arrow=False)

        con_i = Connection.connect_to_line(conv_motor[0], pwm.position.sub_y(1.5), text=r'$i$', arrow=False, fill=False,
                                           draw=0.1)
        inputs = dict(u=[pwm.input_left[0], dict(text=r'$u^{*}$')])
        outputs = dict(i=con_i.end)
        connect_to_lines = dict()
        start = converter.position

        if emf_feedforward or control_task in ['SC']:
            con_omega = Connection.connect(dc_shunt.output_left[0].sub_x(2), dc_shunt.output_left[0],
                                           text=r'$\omega_{me}$', arrow=False)
            outputs['omega'] = con_omega.end

        return start, inputs, outputs, connect_to_lines
    return _series_dc_stage


if __name__ == '__main__':

    env_id = 'Cont-SC-ShuntDc-v0'
    emf_feedforward = True
    document = ControllerDiagram('pdf')
    start = Point(0, 0)

    stages = [omega_stage, torque_stage, current_stage(emf_feedforward, env_id), series_dc_stage(emf_feedforward, env_id)]
    #stages = [current_stage(emf_feedforward, env_id), series_dc_stage(emf_feedforward, env_id)]
    inputs = dict()
    outputs = dict()
    connections = dict()
    connect_to_lines = dict()

    for idx, stage in enumerate(stages):
        start, inputs_, outputs_, connect_to_lines_ = stage(start, idx)
        inputs = {**inputs, **inputs_}
        outputs = {**outputs, **outputs_}
        connect_to_lines = {**connect_to_lines, **connect_to_lines_}

    for key in inputs.keys():
        if key in outputs.keys():
            connections[key] = Connection.connect(outputs[key], inputs[key][0], **inputs[key][1])

    for key in connect_to_lines.keys():
        if key in connections.keys():
            Connection.connect_to_line(connections[key], connect_to_lines[key][0], **connect_to_lines[key][1])

    document.build()
    document.show()

