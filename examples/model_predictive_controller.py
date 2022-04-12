from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Text
from control_block_diagram.predefined_components import Add


if __name__ == '__main__':
    doc = ControllerDiagram('pdf')
    box_plant = Box(Point(0, 0), size=(1.5, 1), text='Plant', inputs=dict(left=2), outputs=dict(right=2))
    Connection.connect(box_plant.input_left[0].sub_x(1.5), box_plant.input_left[0], text='Disturbances',
                       text_position='start')
    color = '{rgb,255:red,85;green,162;blue,171}'
    box_mpc = Box(box_plant.right.add(3, -1.25), size=(5.5, 4.5), fill='{rgb,255:red,177;green,218;blue,236}', draw=None)
    text = Text(text='MPC', position=box_mpc.top.add_y(0.5), text_color=color, text_size='Large')
    box_model = Box(box_plant.right.add_x(3), size=(1.5, 1), inputs=dict(left=2), text='Model')
    Connection.connect(box_plant.output_right[0], box_model.input_left[0], text='Output')
    add = Add(box_model.right.add_x(2.5), inputs=dict(left=1, top=1), outputs=dict(bottom=1))
    con_pred_output = Connection.connect(box_model.output[0], add.input_left[0], text='Predicted\noutput',
                                         distance_y=0.5)
    Text(text='$-$', position=con_pred_output.end.add(-0.2, 0.2))
    con_ref = Connection.connect(add.input_top[0].add_y(1.5), add.input_top[0], text='Reference\ntrajectory',
                                 text_position='start', text_align='left', distance_x=0.8)
    Text(text='$+$', position=con_ref.end.add(0.2, 0.2))

    box_optimizer = Box(box_model.position.sub(0.5, 2), size=(1.8, 1), text='Optimizer', inputs=dict(right=1, bottom=2),
                        outputs=dict(left=1))
    Connection.connect(add.output, box_optimizer.input_right)
    con_input = Connection.connect(box_optimizer.output_left[0], box_plant.input_left[1])
    con_input = Connection.connect_to_line(con_input, box_model.input_left[1].sub_x(1.5), arrow=False, text='Input',
                               text_position='start', move_text=(0.5, 0.5))
    Connection.connect(con_input.end, box_model.input_left[1])
    Connection.connect(box_optimizer.input_bottom[0].sub_y(0.8), box_optimizer.input_bottom[0], text='Constraints',
                       text_align='left', distance_x=1)
    Connection.connect(box_optimizer.input_bottom[1].sub_y(0.8), box_optimizer.input_bottom[1], text=Text('Cost function',
                                                                                                        size=(2.5, 1)),
                       text_align='right', distance_x=1.1)

    doc.build()
    doc.show()