from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Text, Circle, Path
from control_block_diagram.predefined_components import DqToAlphaBetaTransformation, Converter, PMSM,\
    AbcToAlphaBetaTransformation, AlphaBetaToDqTransformation, Add, PIController, Multiply, DcShuntMotor, DcSeriesMotor,\
    DcConverter, DcPermExMotor, Divide, DcExtExMotor, IController


class PsiOptBox(Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bx = 0.1
        by = 0.15
        Connection.connect(self.bottom_left.add(self._size_x * bx, self._size_y * by),
                           self.bottom_right.add(-self._size_x * bx, self._size_y * by))
        Connection.connect(self.bottom.add_y(self._size_y * by), self.top.sub_y(self._size_y * by))
        Path([self.top_left.add(self._size_x * bx, -self._size_y * (0.1 + by)),
              self.bottom.add_y(self._size_y * (0.2 + by)),
              self.top_right.sub(self._size_x * bx, self._size_y * (0.1 + by))],
             angles=[{'in': 180, 'out': 0}, {'in': 180, 'out': 0}], arrow=False)


class LimitBox(Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bx = 0.1
        by = 0.1
        le = (1 - 2 * bx) / 3

        Connection([self.bottom_left.add(self._size_x * bx, self._size_y * by),
                    self.bottom_left.add(self._size_x * bx + le, self._size_y * by),
                    self.top_right.sub(self._size_x * bx + le, self._size_y * by),
                    self.top_right.sub(self._size_x * bx, self._size_y * by)], arrow=False)


class TMaxPsiBox(Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bx = 0.1 * self._size_x
        by = 0.15 * self._size_y
        scale = 1.5

        Connection.connect(self.bottom_left.add(bx, by), self.top_left.add(bx, -by))
        Connection.connect(self.left.add_x(bx), self.right.sub_x(bx))
        Path([self.left.add_x(bx), self.top_right.sub(scale * bx, scale * by)], arrow=False,
             angles=[{'in': 180, 'out': 35}])
        Path([self.left.add_x(bx), self.bottom_right.add(-scale * bx, scale * by)], arrow=False,
             angles=[{'in': 180, 'out': -35}])


def omega_stage(start, control_task):
    space = 1 if control_task == 'SC' else 1.5
    add_omega = Add(start.add_x(space))
    Connection.connect(add_omega.input_bottom[0].sub_y(1), add_omega.input_bottom[0], text=r'$\omega_{\mathrm{me}}$',
                       text_align='bottom', text_position='start')
    if control_task == 'SC':
        Connection.connect(start, add_omega.input_left[0], text=r'$\omega^{*}$', text_align='left',
                           text_position='start')
    pi_omega = PIController(add_omega.position.add_x(1.5), text='Speed\nController')
    Connection.connect(add_omega.output_right, pi_omega.input_left)

    start = pi_omega.output_right[0]
    inputs = dict(omega_ref=[add_omega.input_left[0], dict(text=r'$\omega^{*}$')])
    outputs = dict(t_ref=pi_omega.output_right[0])
    connect_to_lines = dict()
    connections = dict()

    return start, inputs, outputs, connect_to_lines, connections


def torque_stage(start, control_task):

    # Torque Controller
    if control_task == 'TC':
        Connection.connect(start, start.add_x(1), text='$T^{*}$', text_position='start', text_align='left', arrow=False)

    box_limit = LimitBox(start.add_x(6), inputs=dict(left=1, bottom=1), size=(1, 1))
    box_psi_opt = PsiOptBox(start.add(2, -1.7), size=(1.2, 1))
    Text(position=box_psi_opt.top.add_y(0.25), text=r'$\Psi^{*}_{\mathrm{opt}}(T^{*})$')
    box_min = Box(box_psi_opt.position.add(1.5, -1.3), inputs=dict(left=2, left_space=0.5), size=(0.8, 1), text='min')
    box_t_max = TMaxPsiBox(box_psi_opt.position.add_x(3.1), size=(1.2, 1))
    Text(position=box_t_max.top.add_y(0.25), text=r'$T_{\mathrm{max}}(\Psi)$')
    con_torque = Connection.connect(start.add_x(1), box_limit.input_left[0])
    Connection.connect(start.add_x(1), box_psi_opt.input_left[0], start_direction='south')
    Circle(start.add_x(1), radius=0.05, fill='black')
    Connection.connect(box_psi_opt.output_right[0], box_min.input_left[0])
    Connection.connect(box_min.output_right[0].add_x(0.3), box_t_max.input_left[0], start_direction='north')
    Circle(box_min.output_right[0].add_x(0.3), radius=0.05, fill='black')
    Connection.connect(box_t_max.output_right[0], box_limit.input_bottom[0])
    box_f_psi_t = Box(box_limit.position.add(2.2, -1.5), size=(1.3, 3.5), inputs=dict(left=2, left_space=3),
                      outputs=dict(right=3, right_space=1), text=r'\textbf{f}($\Psi$, $T$)')

    Connection.connect(box_min.output_right[0], box_f_psi_t.input_left[1], text=r'$\Psi^{*}_{\mathrm{lim}}$')
    Connection.connect(box_limit.output_right[0], box_f_psi_t.input_left[0], text=r'$T^{*}_{\mathrm{lim}}$')

    # Moulation Controller
    add_psi = Add(box_min.input_left[1].sub_x(1))
    Connection.connect(add_psi.output_right[0], box_min.input_left[1], text=r'$\Psi_{\mathrm{lim}}$', text_align='top',
                       distance_y=0.25)
    i_controller = IController(add_psi.input_left[0].sub_x(1.5), size=(1.2, 1), text='Modulation\nController')
    Connection.connect(i_controller.output_right[0], add_psi.input_left[0], text=r'$\Delta \Psi$', distance_y=0.25)
    add_a = Add(i_controller.position.sub_x(1.5))
    Connection.connect(add_a.output_right[0], i_controller.input_left[0])
    box_a_max = Box(add_a.input_left[0].sub_x(1.3), size=(1.5, 0.8), text=r'$a_{\mathrm{max}} \cdot k$')
    Connection.connect(box_a_max.output_right[0], add_a.input_left[0], text='$a^{*}$')
    box_abs = Box(add_a.position.sub_y(1.2), size=(0.8, 0.8), text=r'|\textbf{x}|', inputs=dict(bottom=1),
                  outputs=dict(top=1))
    con_a = Connection.connect(box_abs.output_top[0], add_a.input_bottom[0], text='$-$', text_align='right', text_position='end',
                       move_text=(-0.1, -0.2))
    Text(position=Point.get_mid(*con_a.points).sub_x(0.25), text='$a$')

    div_a = Divide(box_abs.input_bottom[0].sub_y(1), size=(1, 0.5), inputs='bottom', input_space=0.5)
    Connection.connect(div_a.input_bottom[0].sub_y(0.7), div_a.input_bottom[0], text=r'$\mathbf{u^{*}_{\mathrm{dq}}}$',
                       text_position='start', text_align='bottom')
    Connection.connect(div_a.input_bottom[1].sub_y(0.7), div_a.input_bottom[1], text=r'$\frac{u_{\mathrm{dc}}}{2}$',
                       text_position='start', text_align='bottom')
    Connection.connect(div_a.output_top[0], box_abs.input_bottom[0])

    div_psi = Divide(add_psi.input_bottom[0].sub_y(2), size=(1, 0.5), inputs='bottom', input_space=0.5)
    Connection.connect(div_psi.output_top[0], add_psi.input_bottom[0], text=r'$\Psi_{\mathrm{max}}$',
                       text_align='right', distance_x=0.5)
    Connection.connect(div_psi.input_bottom[0].sub_y(0.7), div_psi.input_bottom[0],
                       text=r'$\frac{u_{\mathrm{dc}}}{\sqrt{3}}$', text_position='start', text_align='bottom')

    # In-/ Outputs
    inputs = dict(t_ref=[con_torque.begin, dict(arrow=False, text=r'$T^{*}$')],
                  omega=[div_psi.input_bottom[1], dict(text=r'$\omega_{\mathrm{el}}$', move_text=(3, 0))])
    outputs = dict(i_d_ref=box_f_psi_t.output_right[0], i_q_ref=box_f_psi_t.output_right[1])
    connect_to_lines = dict()
    connections = dict()
    start = box_f_psi_t.output_right[0]

    return start, inputs, outputs, connect_to_lines, connections


def current_stage(emf_feedforward):
    def _current_stage(start, control_task):
        space = 1 if control_task == 'CC' else 1.5
        add_i_sd = Add(start.add_x(space))
        add_i_sq = Add(add_i_sd.position.sub(0.5, 1))

        if control_task == 'CC':
            Connection.connect(add_i_sd.input_left[0].sub_x(space), add_i_sd.input_left[0],
                               text=r'$i^{*}_{\mathrm{sd}}$', text_position='start', text_align='left')
            Connection.connect(add_i_sq.input_left[0].sub_x(space - 0.5), add_i_sq.input_left[0],
                               text=r'$i^{*}_{\mathrm{sq}}$', text_position='start', text_align='left')

        pi_i_sd = PIController(add_i_sd.position.add_x(1.2), size=(1, 0.8), input_number=1, output_number=1,
                               text='Current\nController')
        pi_i_sq = PIController(Point.merge(pi_i_sd.position, add_i_sq.position), size=(1, 0.8), input_number=1,
                               output_number=1)

        Connection.connect(add_i_sd.output_right, pi_i_sd.input_left)
        Connection.connect(add_i_sq.output_right, pi_i_sq.input_left)

        add_u_sd = Add(pi_i_sd.position.add_x(2))
        add_u_sq = Add(pi_i_sq.position.add_x(1.2))

        Connection.connect(pi_i_sd.output_right[0], add_u_sd.input_left[0], text=r'$\Delta u^{*}_{\mathrm{sd}}$',
                           distance_y=0.28)
        Connection.connect(pi_i_sq.output_right[0], add_u_sq.input_left[0], text=r'$\Delta u^{*}_{\mathrm{sq}}$',
                           distance_y=0.4, move_text=(0.25, 0))

        dq_to_alpha_beta = DqToAlphaBetaTransformation(Point.get_mid(add_u_sd.position, add_u_sq.position).add_x(2),
                                                       input_space=1)

        Connection.connect(add_u_sd.output_right[0], dq_to_alpha_beta.input_left[0], text=r'$u^{*}_{\mathrm{sd}}$',
                           distance_y=0.28)
        Connection.connect(add_u_sq.output_right[0], dq_to_alpha_beta.input_left[1], text=r'$u^{*}_{\mathrm{sq}}$',
                           distance_y=0.28, move_text=(0.4, 0))

        pwm = Box(dq_to_alpha_beta.position.add_x(2.5), size=(1.5, 1.2), text='PWM',
                  inputs=dict(left=2, left_space=0.6),
                  outputs=dict(right=3, right_space=0.3))

        Connection.connect(dq_to_alpha_beta.output_right, pwm.input_left,
                           text=[r'$u^*_{\mathrm{s} \upalpha}$', r'$u^*_{\mathrm{s} \upbeta}$'], distance_y=0.25)

        abc_to_alpha_beta = AbcToAlphaBetaTransformation(pwm.position.sub_y(3.5), input='right', output='left')

        alpha_beta_to_dq = AlphaBetaToDqTransformation(
            Point.merge(dq_to_alpha_beta.position, abc_to_alpha_beta.position), input='right', output='left')

        distance = (add_u_sq.position.y - alpha_beta_to_dq.output_left[0].y) / 4

        multiply_u_sq = Multiply(add_u_sq.position.sub_y(distance), outputs=dict(top=1))
        Connection.connect(multiply_u_sq.output_top, add_u_sq.input_bottom)

        add_psi_p = Add(multiply_u_sq.position.sub_y(distance), outputs=dict(top=1))
        Connection.connect(add_psi_p.output_top, multiply_u_sq.input_bottom)
        Connection.connect(add_psi_p.input_left[0].sub_x(0.3), add_psi_p.input_left[0], text=r'$\Psi_{\mathrm{p}}$',
                           text_position='start', text_align='left', distance_x=0.25)

        box_ls_1 = Box(add_psi_p.position.sub_y(distance), size=(0.6, 0.6), inputs=dict(bottom=1), outputs=dict(top=1),
                       text=r'$L_{\mathrm{s}}$')
        Connection.connect(box_ls_1.output_top, add_psi_p.input_bottom)

        multiply_u_sd = Multiply(Point.merge(add_u_sd.position, multiply_u_sq.position), outputs=dict(top=1))
        Connection.connect(multiply_u_sd.output_top, add_u_sd.input_bottom, text=r'-', text_position='end',
                           text_align='right', move_text=(-0.2, -0.2))
        Connection.connect(multiply_u_sd.input_left[0].sub_x(0.3), multiply_u_sd.input_left[0])

        box_ls_2 = Box(Point.merge(multiply_u_sd.position, box_ls_1.position), size=(0.6, 0.6), inputs=dict(bottom=1),
                       outputs=dict(top=1), text=r'$L_{\mathrm{s}}$')
        Connection.connect(box_ls_2.output_top, multiply_u_sd.input_bottom)

        con_3 = Connection.connect(alpha_beta_to_dq.output_left[0], add_i_sd.input_bottom[0], text=r'-',
                                   text_position='end',
                                   text_align='right', move_text=(-0.2, -0.2))
        Connection.connect_to_line(con_3, box_ls_1.input_bottom[0])

        con_4 = Connection.connect(alpha_beta_to_dq.output_left[1], add_i_sq.input_bottom[0], text=r'-',
                                   text_position='end',
                                   text_align='right', move_text=(-0.2, -0.2))
        Connection.connect_to_line(con_4, box_ls_2.input_bottom[0])

        box_d_dt = Box(Point.merge(alpha_beta_to_dq.position, start.sub_y(6.57020066645696)).sub_x(2), size=(1, 0.8),
                       text=r'$\mathrm{d} / \mathrm{d}t$', inputs=dict(right=1), outputs=dict(left=1))

        con_omega = Connection.connect(box_d_dt.output_left, multiply_u_sq.input_left, space_y=1,
                                       text=r'$\omega_{\mathrm{el}}$', move_text=(0, 2), text_align='left',
                                       distance_x=0.3)

        if control_task == 'SC':
            Circle(con_omega[0].points[1], radius=0.05, fill='black')

        Connection.connect(abc_to_alpha_beta.output, alpha_beta_to_dq.input_right,
                           text=[r'$i_{\mathrm{s} \upalpha}$', r'$i_{\mathrm{s} \upbeta}$'])

        add = Add(Point.get_mid(dq_to_alpha_beta.position, alpha_beta_to_dq.position), inputs=dict(bottom=1, right=1),
                  outputs=dict(top=1))

        Connection.connect(alpha_beta_to_dq.output_top, add.input_bottom, text=r'$\varepsilon_{\mathrm{el}}$',
                           text_align='right', move_text=(0, -0.1))
        Connection.connect(add.output_top, dq_to_alpha_beta.input_bottom)

        box_t_a = Box(add.position.add_x(1.5), size=(1, 0.8), text=r'$1.5 T_{\mathrm{s}}$', inputs=dict(right=1),
                      outputs=dict(left=1))

        Connection.connect(box_t_a.output, add.input_right, text=r'$\Delta \varepsilon$')
        Connection.connect(box_t_a.input[0].add_x(0.5), box_t_a.input[0], text=r'$\omega_{el}$',
                                       text_position='start', text_align='right', distance_x=0.3)

        start = pwm.position
        inputs = dict(i_d_ref=[add_i_sd.input_left[0], dict(text=r'$i^{*}_{\mathrm{sd}}$', distance_y=0.25)],
                      i_q_ref=[add_i_sq.input_left[0], dict(text=r'$i^{*}_{\mathrm{sq}}$', distance_y=0.25)],
                      epsilon=[box_d_dt.input_right[0], dict()])

        outputs = dict(S=pwm.output_right, omega=con_omega[0].points[1])
        connect_to_line = dict(epsilon=[alpha_beta_to_dq.input_bottom[0], dict(text=r'$\varepsilon_{\mathrm{el}}$',
                                                                               text_position='middle',
                                                                               text_align='right')],
                               i=[abc_to_alpha_beta.input_right, dict(draw=0.1, fill=False,
                                                                      text=[r'$\mathbf{i}_{\mathrm{s a,b,c}}$', '',
                                                                            ''])])
        connections = dict()

        return start, inputs, outputs, connect_to_line, connections

    return _current_stage


def series_dc_stage(emf_feedforward):
    def _series_dc_stage(start, control_task):
        converter = DcConverter(start.add_x(2.7), input_number=3, input_space=0.3, output_number=3)
        pmsm = PMSM(converter.position.sub_y(5), size=1.3, input='top')
        con_1 = Connection.connect(converter.output_bottom, pmsm.input_top, arrow=False)

        start = pmsm.position
        inputs = dict(S=[converter.input_left, dict(text=[r'$\mathbf{S}_{\mathrm{a,b,c}}$', '', ''], distance_y=0.25)])
        outputs = dict(epsilon=pmsm.output_left[0])
        connect_to_lines = dict()
        connections = dict(i=con_1)

        return start, inputs, outputs, connect_to_lines, connections

    return _series_dc_stage


if __name__ == '__main__':

    env_id = 'DqCont-CC-PMSM-v0'
    control_task = env_id.split('-')[1]
    emf_feedforward = True
    document = ControllerDiagram('pdf')
    start = Point(0, 0)

    stages = [omega_stage, torque_stage, current_stage(emf_feedforward), series_dc_stage(emf_feedforward)]
    stages = [current_stage(emf_feedforward), series_dc_stage(emf_feedforward)]

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

