from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Text
from control_block_diagram.predefined_components import DqToAlphaBetaTransformation, Converter, PMSM,\
    AbcToAlphaBetaTransformation, AlphaBetaToDqTransformation, Add, PIController


if __name__ == '__main__':

    document = ControllerDiagram()
    ControllerDiagram.set_document(document)

    pi_controller = PIController(Point(0, 0))
    dq_to_alpha_beta = DqToAlphaBetaTransformation(pi_controller.position.add_x(2.5))
    pwm = Box(dq_to_alpha_beta.position.add_x(2.5), size=(1.5, 1.2), text='PWM', inputs=dict(left=2, left_space=0.6),
              outputs=dict(right=3, right_space=0.3))

    Connection.connect(dq_to_alpha_beta.output_right, pwm.input_left, text=[r'$u^*_{s \alpha}$', r'$u^*_{s \beta}$'])

    converter = Converter(pwm.position.add_x(2.5), input='left', input_number=3, input_space=0.3, output='bottom',
                          output_number=3, additional_inputs=dict(top=2, top_space=0.8))

    Connection.connect(pwm.output_right, converter.input_left, text=['$S_{a,b,c}$', '', ''])
    con_1 = [Connection.connect(input.add_y(0.7), input, arrow=False) for input in converter.input_top]
    Connection.connect(con_1[1].begin.add(-0.1, 0.1), con_1[0].begin.add(0.1, 0.1), text=r'$u_{dc}$')

    pmsm = PMSM(converter.position.sub_y(5), size=1.3, input='top')
    con_2 = Connection.connect(converter.output_bottom, pmsm.input_top, arrow=False)

    abc_to_alpha_beta = AbcToAlphaBetaTransformation(pwm.position.sub_y(3.5), size=1.2, input='right', output='left')

    Connection.connect_to_line(con_2, abc_to_alpha_beta.input_right, draw=0.1, fill=False, text=[r'$i_{s a,b,c}$', '', ''])

    alpha_beta_to_dq = AlphaBetaToDqTransformation(Point.merge(dq_to_alpha_beta.position, abc_to_alpha_beta.position),
                                                   size=1.2, input='right', output='left')

    con_3 = Connection.connect(pmsm.output_left, alpha_beta_to_dq.input_bottom, text=r'$\varepsilon$', text_position=(1, 'middle'),
                       text_align='right')

    Connection.connect(abc_to_alpha_beta.output, alpha_beta_to_dq.input_right, text=[r'$i_{s \alpha}$', r'$i_{s \beta}$'])

    add = Add(Point.get_mid(dq_to_alpha_beta.position, alpha_beta_to_dq.position), inputs=dict(bottom=1, right=1),
              outputs=dict(top=1))

    Connection.connect(alpha_beta_to_dq.output_top, add.input_bottom, text=r'$\epsilon$', text_align='right')
    Connection.connect(add.output_top, dq_to_alpha_beta.input_bottom)

    box_T_a = Box(add.position.add_x(1.5), size=(1, 0.8), text=r'$1,5 T_a$', inputs=dict(right=1), outputs=dict(left=1))

    Connection.connect(box_T_a.output, add.input_right, text=r'$\Delta \epsilon$')
    Connection.connect(box_T_a.input[0].add_x(0.5), box_T_a.input[0], text=r'$\omega$', text_position='start',
                       text_align='right', distance_x=0.2)

    top_left = Point(add.border['left'], box_T_a.border['top']).add(-0.1, 0.1)
    bottom_right = box_T_a.bottom_right.add(0.1, -0.1)
    box_winkelvorhalt = Box([top_left, bottom_right], fill=False, draw='blue')

    text_winkelvorhalt = Text('Winkelvorhalt', position=box_winkelvorhalt.bottom_right.sub_y(0.2))

    document.build()
    document.show()

