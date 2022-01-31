from control_block_diagram import *


diagram = ControllerDiagram()

text_1 = Text(['EMF Feedforward'], Point(3.5, 1), size=(5, 2), doc=diagram)

connection_1 = Connection([Point(0, 0), Point(1, 0)], text=r'$\underline{u}^*$', distance_y=0.3, doc=diagram)

box_select = Box(Point(1, -1.5), (1, 1.5), Text(['Select']), outputs=dict(right=2, right_space=0.3), doc=diagram)
connection_2 = Connection.connect(box_select.input_left[0].add_x(-1), box_select.input_left[0], text=r'$\underline{s}$',
                                  doc=diagram)

circle_1 = Circle(box_select.output[1].add_x(1.5), 0.2, Text([r'$\times$']), inputs=dict(left=1, bottom=1), doc=diagram)
connection_3 = Connection.connect(box_select.output[1], circle_1.input_left[0], text=r'$\underline{i}$', doc=diagram)
box_l = Box(Center.convert(circle_1.input_bottom[0].add_y(-1)), (1, 1), Text([r'$\underline{L}$']), inputs=dict(),
            outputs=dict(top=1), doc=diagram)
connection_4 = Connection.connect(box_l.output, circle_1.input_bottom, doc=diagram)

circle_2 = Circle(circle_1.output_right[0].add_x(1.5), 0.2, Text(['+']), inputs=dict(left=1, bottom=1), outputs=dict(top=1),
                  doc=diagram)
connection_5 = Connection.connect(circle_1.output, circle_2.input_left, doc=diagram)
box_psi = Box(Center.convert(circle_2.input_bottom[0].add_y(-1)), (1, 1), Text([r'$\underline{\Psi}$']), inputs=dict(),
              outputs=dict(top=1), doc=diagram)
connection_6 = Connection.connect(box_psi.output, circle_2.input_bottom, doc=diagram)

circle_3 = Circle(Center(circle_2.output_top[0].x, box_select.output_right[0].y), 0.2, Text([r'$\times$']), inputs=dict(bottom=1, left=1),
                  outputs=dict(top=1), doc=diagram)
connection_7 = Connection.connect(box_select.output_right[0], circle_3.input_left[0], text=r'$\omega$', doc=diagram)
connection_8 = Connection.connect(circle_2.output_top, circle_3.input_bottom, doc=diagram)

circle_4 = Circle(Center(circle_3.output_top[0].x, connection_1.end.y), 0.2, Text(['+']), inputs=dict(left=1, bottom=1), doc=diagram)
connection_9 = Connection.connect(connection_1.end, circle_4.input_left[0], doc=diagram)
connection_10 = Connection.connect(circle_3.output_top, circle_4.input_bottom, doc=diagram)
connection_11 = Connection.connect(circle_4.output_right[0], circle_4.output_right[0].add_x(1),
                                   text=r'$\underline{u}^{*}_\mathrm{ff}$', distance_y=0.3, doc=diagram)

diagram.build()
diagram.show()
