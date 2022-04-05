from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Text, Circle, Path
from control_block_diagram.predefined_components import DqToAlphaBetaTransformation, AbcToAlphaBetaTransformation,\
    AlphaBetaToDqTransformation, Add, PIController, DcConverter, Divide, IController, SCIM, Limit


class PsiOptBox(Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bx = 0.1
        by = 0.15
        Connection.connect(self.bottom_left.add(self._size_x * bx, self._size_y * by),
                           self.bottom_right.add(-self._size_x * bx, self._size_y * by))
        Connection.connect(self.bottom.add_y(self._size_y * by), self.top.sub_y(self._size_y * by))
        Path([self.top_left.add(self._size_x * bx, -self._size_y * (0.1 + by)),
              self.bottom.add_y(self._size_y * by),
              self.top_right.sub(self._size_x * bx, self._size_y * (0.1 + by))],
             angles=[{'in': 110, 'out': -20}, {'in': 200, 'out': 70}], arrow=False)


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
    if control_task == 'SC':
        Connection.connect(start, add_omega.input_left[0], text=r'$\omega^{*}$', text_align='left',
                           text_position='start')
    pi_omega = PIController(add_omega.position.add_x(1.5), text='Speed\nController')
    Connection.connect(add_omega.output_right, pi_omega.input_left)
    limit = Limit(pi_omega.output_right[0].add_x(1.5), size=(1.2, 1.2))
    Connection.connect(pi_omega.output_right[0], limit.input_left[0])

    start = limit.output_right[0].add(0.5, 2)
    inputs = dict(omega_ref=[add_omega.input_left[0], dict(text=r'$\omega^{*}$')],
                  omega_me=[add_omega.input_bottom[0], dict(text='-', text_position='end', text_align='right',
                                                         move_text=(-0.2, -0.2))])
    outputs = dict(t_ref=limit.output_right[0])
    connect_to_lines = dict()
    connections = dict()

    return start, inputs, outputs, connect_to_lines, connections


def torque_stage(start, control_task):

    start_add = 0
    # Torque Controller
    if control_task == 'TC':
        start_add = 1
        Connection.connect(start, start.add_x(start_add), text='$T^{*}$', text_position='start', text_align='left', arrow=False)

    box_limit = Limit(start.add_x(start_add + 5), size=(1, 1), inputs=dict(left=1, top=1))
    Connection.connect(start.add_x(start_add), box_limit.input_left[0])
    box_psi_opt = PsiOptBox(start.add(start_add + 1, 1.7), size=(1.2, 1))
    Text(position=box_psi_opt.bottom.sub_y(0.3), text=r'$\Psi^{*}_{\mathrm{opt}}(T^{*})$')
    box_min = Box(box_psi_opt.position.add(1.5, 1.3), inputs=dict(left=2, left_space=0.5), size=(0.8, 1), text='min')
    box_t_max = TMaxPsiBox(box_psi_opt.position.add_x(3.1), size=(1.2, 1))
    Text(position=box_t_max.bottom.sub_y(0.3), text=r'$T_{\mathrm{max}}(\Psi)$')
    Connection.connect(start.add_x(start_add), box_psi_opt.input_left[0], start_direction='north')
    Circle(start.add_x(start_add), radius=0.05, fill='black')
    Connection.connect(box_psi_opt.output_right[0], box_min.input_left[1])
    Connection.connect(box_min.output_right[0].add_x(0.3), box_t_max.input_left[0], start_direction='south')
    Circle(box_min.output_right[0].add_x(0.3), radius=0.05, fill='black')
    Connection.connect(box_t_max.output_right[0], box_limit.input_top[0])

    box_i_sq_ref = Box(box_limit.output_right[0].add_x(1.5), size=(1, 0.8),
                       text=r'$\frac{2 L_{\mathrm{r}}}{3 p L_{\mathrm{m}}}$')
    Connection.connect(box_limit.output_right, box_i_sq_ref.input_left, text=r'$T^{*}_{\mathrm{lim}}$')
    divide = Box(box_i_sq_ref.output_right[0].add_x(1), size=(0.5, 0.5), text=r'$\div$', inputs=dict(left=1, bottom=1),
                 outputs=dict(right=1, top=1))
    Connection.connect(box_i_sq_ref.output_right, divide.input_left)

    add_psi = Add(box_min.output_right[0].add_x(2.5))
    Connection.connect(box_min.output_right, add_psi.input_left, text=r'$\Psi^{*}_{\mathrm{lim}}$')
    Connection.connect(divide.output_top, add_psi.input_bottom, text=r'$\hat{\Psi}_r$')
    pi_psi = PIController(add_psi.position.add_x(1.5), text='Flux\nController')
    Connection.connect(add_psi.output_right, pi_psi.input_left)

    limit = Limit(pi_psi.position.add(3.5, -0.5), size=(1.5, 1.5), inputs=dict(left=2, left_space=1),
                  outputs=dict(right=2, right_space=1))

    Connection.connect(pi_psi.output_right[0], limit.input_left[0])
    Connection.connect(divide.output_right[0], limit.input_left[1])

    # Modulation Controller
    add_a = Add(box_min.input_left[0].sub_x(1.5), inputs=dict(left=1, top=1))
    Connection.connect(add_a.output_right[0], box_min.input_left[0], text=r'$\Psi_{\mathrm{lim}}$', text_align='bottom',
                       distance_y=0.25)
    divide_a = Divide(add_a.position.add_y(1), size=(1, 0.5), inputs='top', input_space=0.5)
    Connection.connect(divide_a.output_bottom, add_a.input_top, text=r'$\Psi_{\mathrm{max}}$', text_align='right',
                       distance_x=0.5)
    Connection.connect(divide_a.input_top[0].add_y(0.3), divide_a.input_top[0],
                       text=r'$\frac{u_{\mathrm{\mbox{\fontsize{3}{4}\selectfont DC}}}}{\sqrt{3}}$', text_position='start',
                       text_align='top')
    Connection.connect(divide_a.input_top[1].add_y(0.3), divide_a.input_top[1], text=r'$\omega_{\mathrm{el}}$',
                       text_position='start', text_align='top', move_text=(0, -0.05))
    limit_psi = Limit(add_a.input_left[0].sub_x(1.5), size=(1, 1))
    Connection.connect(limit_psi.output_right[0], add_a.input_left[0], text=r'$\Delta \Psi$', distance_y=0.25,
                       text_align='bottom')
    i_controller = IController(limit_psi.input_left[0].sub_x(1.2), size=(1.2, 1), text='Modulation\nController')
    Connection.connect(i_controller.output_right, limit_psi.input_left)
    add_a_max = Add(i_controller.position.sub_x(1.5))
    Connection.connect(add_a_max.output_right, i_controller.input_left)
    box_a_max = Box(add_a_max.input_left[0].sub_x(1.3), size=(1.5, 0.8), text=r'$a_{\mathrm{max}} \cdot k$')
    Connection.connect(box_a_max.output_right[0], add_a_max.input_left[0], text='$a^{*}$', text_align='bottom')
    box_abs = Box(add_a_max.input_bottom[0].sub_y(1), size=(0.8, 0.8), text=r'|\textbf{x}|', inputs=dict(bottom=1),
                  outputs=dict(top=1))
    con_a = Connection.connect(box_abs.output_top[0], add_a_max.input_bottom[0], text='$-$', text_align='right',
                               text_position='end', move_text=(-0.1, -0.1))
    Text(position=Point.get_mid(*con_a.points).sub_x(0.25), text='$a$')
    div_a = Divide(box_abs.input_bottom[0].sub_y(0.8), size=(1, 0.5), inputs='bottom', input_space=0.5)
    Connection.connect(div_a.input_bottom[1].sub_y(0.4), div_a.input_bottom[1],
                       text=r'$\frac{u_{\mathrm{\mbox{\fontsize{3}{4}\selectfont DC}}}}{2}$', text_align='bottom',
                       text_position='start')
    Connection.connect(div_a.input_bottom[0].sub_y(0.4), div_a.input_bottom[0],
                       text=r'$\mathbf{u^{*}_{\mathrm{dq}}}$', text_align='bottom', text_position='start')
    Connection.connect(div_a.output_top, box_abs.input_bottom)

    # In-/ Outputs
    inputs = dict(t_ref=[start, dict(arrow=False, text=r'$T^{*}$', end_direction='south', move_text=(-0.25, 1.8))],
                  psi_r=[divide.input_bottom[0], dict()])
    outputs = dict(i_q_ref=limit.output_right[1], i_d_ref=limit.output_right[0])
    connect_to_lines = dict()
    connections = dict()
    start = limit.output_right[0]

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

        limit = Limit(dq_to_alpha_beta.position.add_x(2.5), size=(1.5, 1.5), inputs=dict(left=2, left_space=0.6),
                      outputs=dict(right=2, right_space=0.6))

        Connection.connect(dq_to_alpha_beta.output_right, limit.input_left)

        pwm = Box(limit.position.add_x(2.5), size=(1.5, 1.2), text='PWM',
                  inputs=dict(left=2, left_space=0.6),
                  outputs=dict(right=3, right_space=0.3))

        Connection.connect(limit.output_right, pwm.input_left,
                           text=[r'$u^*_{\mathrm{s} \upalpha}$', r'$u^*_{\mathrm{s} \upbeta}$'], distance_y=0.25)

        abc_to_alpha_beta = AbcToAlphaBetaTransformation(pwm.position.sub(1, 3), input='right', output='left')

        observer = Box(abc_to_alpha_beta.position.sub(0.5, 2.2), size=(2, 1), text='Flux Observer',
                       inputs=dict(right=1, top=2, top_space=1.2), outputs=dict(left=2))
        con_omega = Connection.connect(observer.input_right[0].add_x(1), observer.input_right[0])
        Connection.connect(observer.input_top[0].add_y(0.4), observer.input_top[0],
                           text=r'$\mathbf{i}_{\mathrm{s a,b,c}}$', text_position='start')
        Connection.connect(observer.input_top[1].add_y(0.4), observer.input_top[1],
                           text=r'$\mathbf{u}_{\mathrm{s a,b,c}}$', text_position='start', move_text=(0, -0.05))

        alpha_beta_to_dq = AlphaBetaToDqTransformation(
            Point.merge(dq_to_alpha_beta.position, abc_to_alpha_beta.position), input='right', output='left')

        con_i_sd = Connection.connect(alpha_beta_to_dq.output_left[0], add_i_sd.input_bottom[0], text='-',
                                      text_position='end', text_align='right', move_text=(-0.2, -0.2))
        con_i_sq = Connection.connect(alpha_beta_to_dq.output_left[1], add_i_sq.input_bottom[0], text='-',
                                      text_position='end', text_align='right', move_text=(-0.2, -0.2))

        Text(position=con_i_sd.begin.add(-0.25, 0.25), text=r'$i_{\mathrm{sd}}$')
        Text(position=con_i_sq.begin.add(-0.25, 0.25), text=r'$i_{\mathrm{sq}}$')

        Connection.connect(observer.output_left[0], alpha_beta_to_dq.input_bottom[0])

        Text(position=observer.output_left[0].add(-0.4, 0.3), text=r'$\angle \hat{\underline{\Psi}}_r$')
        Text(position=observer.output_left[1].add(-0.4, -0.3), text=r'$\hat{\Psi}_r$')

        Connection.connect(abc_to_alpha_beta.output, alpha_beta_to_dq.input_right,
                           text=[r'$i_{\mathrm{s} \upalpha}$', r'$i_{\mathrm{s} \upbeta}$'])

        Connection.connect(alpha_beta_to_dq.output_top, dq_to_alpha_beta.input_bottom,
                           text=r'$\angle \hat{\underline{\Psi}}_r$', text_align='right')

        feedforward = Box(Point.get_mid(add_u_sd.position, add_u_sq.position).sub_y(1.6), size=(2, 0.8),
                           text='feedforward', inputs=dict(bottom=4, bottom_space=0.3), outputs=dict(top=2, top_space=0.8))

        con_omega_2 = Connection.connect(feedforward.input_bottom[0].add(7, -4.0702), feedforward.input_bottom[0],
                                         text=r'$\omega_{\mathrm{me}}$', text_position='start', move_text=(-1, -0.1))
        Connection.connect_to_line(con_omega_2, con_omega.begin, arrow=False)
        Connection.connect(feedforward.output_top[0], add_u_sq.input_bottom[0])
        Connection.connect(feedforward.output_top[1], add_u_sd.input_bottom[0])

        con_psi_r = Connection.connect(observer.output_left[1], feedforward.input_bottom[1])
        if control_task in ['TC', 'SC']:
            Circle(con_psi_r.points[1], radius=0.05, draw='black', fill='black')
        if control_task == 'SC':
            Circle(con_omega_2.points[1], radius=0.05, draw='black', fill='black')
        Connection.connect_to_line(con_i_sd, feedforward.input_bottom[2])
        Connection.connect_to_line(con_i_sq, feedforward.input_bottom[3])

        start = pwm.position
        inputs = dict(i_d_ref=[add_i_sd.input_left[0], dict(text=r'$i^{*}_{\mathrm{sd}}$', distance_y=0.3,
                                                            text_position='end', move_text=(-0.85, 0))],
                      i_q_ref=[add_i_sq.input_left[0], dict(text=r'$i^{*}_{\mathrm{sq}}$', distance_y=0.3,
                                                            text_position='end', move_text=(-0.35, 0))],
                      omega=[con_omega_2.begin, dict(arrow=False)])

        outputs = dict(S=pwm.output_right, psi_r=con_psi_r.points[1], omega_me=con_omega_2.points[1])
        connect_to_line = dict(i=[abc_to_alpha_beta.input_right, dict(draw=0.1, fill=False,
                                                                      text=[r'$\mathbf{i}_{\mathrm{s a,b,c}}$', '', ''])])
        connections = dict()

        return start, inputs, outputs, connect_to_line, connections

    return _current_stage


def series_dc_stage(emf_feedforward):
    def _series_dc_stage(start, control_task):
        converter = DcConverter(start.add_x(2.7), input_number=3, input_space=0.3, output_number=3)
        scim = SCIM(converter.position.sub_y(5), size=1.3, input='top')
        con_1 = Connection.connect(converter.output_bottom, scim.input_top, arrow=False)
        start = scim.position
        inputs = dict(S=[converter.input_left, dict(text=[r'$\mathbf{S}_{\mathrm{a,b,c}}$', '', ''], distance_y=0.25)])
        outputs = dict(omega=scim.output_left[0])
        connect_to_lines = dict()
        connections = dict(i=con_1)

        return start, inputs, outputs, connect_to_lines, connections

    return _series_dc_stage


if __name__ == '__main__':

    env_id = 'Cont-SC-SCIM-v0'
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

