from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Text, Circle
from control_block_diagram.predefined_components import DqToAlphaBetaTransformation, Converter, PMSM,\
    AbcToAlphaBetaTransformation, AlphaBetaToDqTransformation, Add, PIController, Multiply, DcShuntMotor, DcSeriesMotor,\
    DcConverter, DcPermExMotor, Divide, DcExtExMotor


def omega_stage(start, control_task):
    space = 1 if control_task == 'SC' else 1.5
    add_omega = Add(start.add_x(space))
    if control_task == 'SC':
        Connection.connect(start, add_omega.input_left[0], text=r'$\omega^{*}$', text_align='left',
                           text_position='start')
    pi_omega = PIController(add_omega.position.add_x(1.5), text='Speed\nController')
    Connection.connect(add_omega.output_right, pi_omega.input_left)

    start = pi_omega.output_right[0]
    inputs = dict(omega_ref=[add_omega.input_left[0], dict(text=r'$\omega^{*}$')], omega=[add_omega.input_bottom[0],
                                        dict(text=r'-', move_text=(-0.2, -0.2), text_position='end',
                                             text_align='right')])
    outputs = dict(t_ref=pi_omega.output_right[0])
    connect_to_lines = dict()
    connections = dict()

    return start, inputs, outputs, connect_to_lines, connections


def torque_stage(start, control_task):
    inp = start.add_x(1)
    Circle(inp, radius=0.05, fill='black')
    box_abs = Box(inp.add(1, 1), size=(0.8, 0.8), text=r'|x|')
    Connection.connect(inp, box_abs.input_left[0], start_direction='north')

    if control_task == 'TC':
        Connection.connect(start, inp, text=r'$T^{*}$', text_align='left',
                           text_position='start', arrow=False)

    multiply = Multiply(box_abs.position.add_x(1.5), size=(0.8, 0.8), inputs=dict(left=1, top=1))
    Connection.connect(box_abs.output_right, multiply.input_left)
    box_rl = Box(multiply.position.add_y(1.2), size=(1.5, 0.8), text=r"$\sqrt{\frac{R_a}{R_e}}L'_e$",
                 outputs=dict(bottom=1))
    Connection.connect(box_rl.output_bottom, multiply.input_top)
    box_sqrt = Box(multiply.position.add_x(1.5), size=(0.8, 0.8), text=r'$\sqrt{x}$')
    Connection.connect(multiply.output_right, box_sqrt.input_left)

    divide_1 = Divide(multiply.position.sub_y(2.3), size=(0.8, 1.2), input_space=0.6)
    Connection.connect(inp, divide_1.input_left[0], start_direction='south')
    box_le = Box(divide_1.input_left[1].sub_x(1), size=(0.8, 0.8), text=r"$L'_e$")
    Connection.connect(box_le.output_right[0], divide_1.input_left[1])
    divide_2 = Divide(divide_1.output_right[0].add(3, 0.3), size=(0.8, 1.2), input_space=0.6)
    Connection.connect(divide_1.output_right[0], divide_2.input_left[1])
    con_sqrt = Connection.connect(box_sqrt.output_right[0], box_sqrt.output_right[0].add_x(2), arrow=False)
    Connection.connect_to_line(con_sqrt, divide_2.input_left[0].sub_x(0.5), arrow=False)
    Connection.connect(divide_2.input_left[0].sub_x(0.5), divide_2.input_left[0])

    inputs = dict(t_ref=[inp, dict(text=r'$T^{*}$', arrow=False)])
    outputs = dict(i_e_ref=con_sqrt.end, i_a_ref=divide_2.output_right[0])
    connect_to_lines = dict()
    connections = dict()
    start = con_sqrt.end

    return start, inputs, outputs, connect_to_lines, connections


def current_stage(emf_feedforward):
    def _current_stage(start, control_task):

        space = 1 if control_task == 'CC' else 1
        add_i_e = Add(start.add_x(space))
        start_i_a = start.sub_y(2)
        add_i_a = Add(start_i_a.add_x(space))

        if control_task == 'CC':
            Connection.connect(start, add_i_e.input_left[0], text=r'$i^{*}_{\mathrm{e}}$', text_align='left',
                               text_position='start')
            Connection.connect(start_i_a, add_i_a.input_left[0], text=r'$i^{*}_{\mathrm{a}}$', text_align='left',
                               text_position='start')
        pi_i_e = PIController(add_i_e.position.add_x(1.5), text='Current\nController')
        Connection.connect(add_i_e.output_right, pi_i_e.input_left)

        pi_i_a = PIController(add_i_a.position.add_x(1.5))
        Connection.connect(add_i_a.output_right, pi_i_a.input_left)

        inputs = dict(i_e_ref=[add_i_e.input_left[0], dict(text=r'$i^{*}_{\mathrm{e}}$', move_text=(-0.1, 0.1))],
                      i_a_ref=[add_i_a.input_left[0], dict(text=r'$i^{*}_{\mathrm{a}}$', move_text=(-0.1, 0.1))],
                      i_a=[add_i_a.input_bottom[0], dict(text=r'-', move_text=(-0.2, -0.2), text_position='end',
                                                         text_align='right')],
                      i_e=[add_i_e.input_bottom[0], dict(text=r'-', move_text=(-0.2, -0.2), text_position='end',
                                                         text_align='right')])
        connect_to_lines = dict()

        if emf_feedforward:
            add_psi = Add(pi_i_a.position.add_x(2))
            Connection.connect(pi_i_a.output_right, add_psi.input_left, text=r'$\Delta u_{\mathrm{a}}$',
                               distance_y=0.25)
            box_psi = Box(add_psi.position.sub_y(2), size=(0.8, 0.8), text=r"$\Psi'_{\mathrm{e}}$",
                          inputs=dict(bottom=1), outputs=dict(top=1))
            Connection.connect(box_psi.output_top, add_psi.input_bottom, text=r'$u_0$', text_position='end',
                               text_align='right', move_text=(0.1, -0.2))
            pwm_a = Box(add_psi.position.add_x(1.8), size=(1.2, 0.8), text='PWM')
            Connection.connect(add_psi.output_right, pwm_a.input_left, text=r'$u_{\mathrm{a}}$', distance_y=0.25)
            if control_task in ['CC', 'TC']:
                inputs['omega'] = [box_psi.input_bottom[0], dict()]
            elif control_task == 'SC':
                connect_to_lines['omega'] = [box_psi.input_bottom[0], dict(section=0)]
        else:
            pwm_a = Box(pi_i_a.position.add_x(2), size=(1.2, 0.8), text='PWM')
            Connection.connect(pi_i_e.output_right, pwm_a.input_left, text=r'$u_{\mathrm{a}}$', distance_y=0.25)

        pwm_e = Box(Point.merge(pwm_a.position, pi_i_e.position), size=(1.2, 0.8), text='PWM')
        Connection.connect(pi_i_e.output_right, pwm_e.input_left, text=r'$u_{\mathrm{e}}$', distance_y=0.25)

        start = pwm_e.position
        outputs = dict(u_e=pwm_e.output_right[0], u_a=pwm_a.output_right[0])

        connections = dict()

        return start, inputs, outputs, connect_to_lines, connections

    return _current_stage


def series_dc_stage(emf_feedforward):
    def _series_dc_stage(start, control_task):
        converter_e = Converter(start.add_x(3.5), size=1.2, input='left', output='bottom', input_number=1,
                                output_number=2)
        converter_a = Converter(start.add(2, -2), size=1.2, input='left', output='bottom', input_number=1,
                                output_number=2)

        dc_ext_ex = DcExtExMotor(converter_a.position.sub_y(3), size=1.2, input=['top', 'right'], output='left')

        con_conv_a = Connection.connect(converter_a.output_bottom[0], dc_ext_ex.input_top[0], arrow=False)
        Connection.connect(converter_a.output_bottom[1], dc_ext_ex.input_top[1], arrow=False, text=r'$i_{\mathrm{e}}$',
                           text_align='right')
        con_conv_e = Connection.connect(converter_e.output_bottom[0], dc_ext_ex.input_right[0], arrow=False)
        Connection.connect(converter_e.output_bottom[1], dc_ext_ex.input_right[1], arrow=False,
                           text=r'$i_{\mathrm{e}}$', text_align='right', move_text=(0, 2))

        con_e = Connection.connect_to_line(con_conv_e, start.sub_y(0.9), arrow=False, draw=0.1, fill=False,
                                           text=r'$i_{\mathrm{e}}$', distance_y=0.25)
        con_a = Connection.connect_to_line(con_conv_a, start.sub_y(2.9), arrow=False, draw=0.1, fill=False,
                                           text=r'$i_{\mathrm{a}}$', distance_y=0.25, text_align='bottom')

        start = converter_a.position
        inputs = dict(u_e=[converter_e.input_left[0], dict(text='S', distance_y=0.25)],
                      u_a=[converter_a.input_left[0], dict(text='S', distance_y=0.25)])
        outputs = dict(i_e=con_e.end, i_a=con_a.end)
        connect_to_lines = dict()
        connections = dict()

        if emf_feedforward or control_task in ['SC']:
            con_omega = Connection.connect(dc_ext_ex.output_left[0].sub_x(2), dc_ext_ex.output_left[0],
                               text=r'$\omega_{\mathrm{me}}$', arrow=False)
            outputs['omega'] = con_omega.end

        return start, inputs, outputs, connect_to_lines, connections
    return _series_dc_stage


if __name__ == '__main__':

    env_id = 'Cont-SC-ExtExDc-v0'
    control_task = env_id.split('-')[1]
    emf_feedforward = True
    document = ControllerDiagram('pdf')
    start = Point(0, 0)

    stages = [omega_stage, torque_stage, current_stage(emf_feedforward), series_dc_stage(emf_feedforward)]

    inputs = dict()
    outputs = dict()
    connections = dict()
    connect_to_lines = dict()

    for idx, stage in enumerate(stages):
        start, inputs_, outputs_, connect_to_lines_, connections_ = stage(start, control_task)
        inputs = {**inputs, **inputs_}
        outputs = {**outputs, **outputs_}
        connect_to_lines = {**connect_to_lines, **connect_to_lines_}
        connections = {**connections, **connections_}

    for key in inputs.keys():
        if key in outputs.keys():
            connections[key] = Connection.connect(outputs[key], inputs[key][0], **inputs[key][1])

    for key in connect_to_lines.keys():
        if key in connections.keys():
            Connection.connect_to_line(connections[key], connect_to_lines[key][0], **connect_to_lines[key][1])

    document.build()
    document.show()

