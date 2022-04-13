from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Text


if __name__ == '__main__':

    # Initialize a new block diagram
    doc = ControllerDiagram()

    # Add components to the document
    box_fpga = Box(Point(4, 0), size=(9.5, 7), fill='{rgb,255:red,200;green,200;blue,200}')
    Text(text='FPGA', position=box_fpga.top.add_y(0.5), text_size=r'\Huge')
    box_serial_int = Box(Point(0, 0), size=(1, 3), text='Serial Interface', fill='black',
                         text_configuration=dict(size=(3, 1), rotate=90, text_color='white'),
                         inputs=dict(left=1, right=3, right_space=1), outputs=dict(right=3, right_space=1))
    Connection.connect(box_serial_int.input_left[0].sub_x(1.5), box_serial_int.input_left[0], text='Data',
                       text_position='start', text_align='top', move_text=(0.5, 0))

    box_loop_controller = Box(box_fpga.position, size=(2, 2), text='Loop\nController', fill='black',
                              text_configuration=dict(text_color='white'), inputs=dict(left=1, top=2, top_space=1,
                              right=2, right_space=1.5, bottom=1), outputs=dict(right=2, right_space=1.5))
    Connection.connect(box_serial_int.output_right[1], box_loop_controller.input_left[0],
                       text=Text('Parameters'), draw='black!70', line_width='very thick')
    box_memory = Box(box_loop_controller.position.add_y(2.5), size=(2, 1), fill='black', text='Memory',
                     text_configuration=dict(text_color='white'), inputs=dict(left=1, right=2, right_space=0.6),
                     outputs=dict(bottom=2, bottom_space=1))
    Connection.connect(Point.get_mid(box_serial_int.output_right[0], box_memory.input_left[0]),
                       box_memory.input_left[0], start_direction='north',
                       text=Text('Measured data/\nNon-linear\ncontrol', size=(2.5, 1.5)),
                       text_align='left', distance_x=1.2, draw='black!70', line_width='very thick')
    Connection.connect(Point.get_mid(box_serial_int.output_right[0], box_memory.input_left[0]),
                       box_serial_int.input_right[0], start_direction='south', draw='black!70', line_width='very thick')
    Connection.connect(box_memory.output_bottom[0], box_loop_controller.input_top[0], text_align='right',
                       draw='black!70', text=Text('$K(t)$'), distance_x=0.4,
                       line_width='very thick')
    Connection.connect(box_memory.output_bottom[1], box_loop_controller.input_top[1], text_align='right',
                       draw='black!70', text=Text(r'$r_{\mathrm{arb}}(t)$'), distance_x=0.6,
                       line_width='very thick')

    box_ramp_gen = Box(box_loop_controller.position.sub_y(2.5), size=(2, 1), fill='black', text='Ramp\nGenerator',
                       text_configuration=dict(text_color='white'), outputs=dict(top=1))
    Connection.connect(box_serial_int.output_right[2], box_ramp_gen.input_left[0],
                       text=Text('Linear\nRamp\nParameters', size=(2.5, 1.5)),
                       distance_y=1.2, text_align='left', move_text=(-0.3, -0.6), draw='black!70', line_width='very thick')
    Connection.connect(box_ramp_gen.output_top, box_loop_controller.input_bottom, text_align='right', draw='black!70',
                       text=Text(r'$r_{\mathrm{lin}}(t)$'), distance_x=0.6, line_width='very thick')
    box_spi_1 = Box(box_memory.right.add(2.5, -0.1), size=(1.2, 1.2), fill='black', text='SPI\nDriver',
                    text_configuration=dict(text_color='white'), inputs=dict(right=1),
                    outputs=dict(left=2, left_space=0.8))
    Connection.connect(box_spi_1.output_left[0], box_memory.input_right[0], text=Text('$m(t)$'),
                       draw='black!70', line_width='very thick')
    Connection.connect(box_spi_1.input_right[0].add_x(1.5), box_spi_1.input_right[0], text='Validation',
                       text_position='start', line_width='very thick')

    box_spi_2 = Box(box_loop_controller.input_right[0].add(2.5, 0.1), size=(1.2, 1.2), fill='black', text='SPI\nDriver',
                    text_configuration=dict(text_color='white'), inputs=dict(right=1), outputs=dict(left=1))
    Connection.connect(box_spi_2.output_left[0], box_loop_controller.input_right[0], draw='black!70',
                       text=Text('$y(t)$'), move_text=(0.5, 0.1), line_width='very thick')
    Connection.connect(box_spi_2.output_left[0], box_memory.input_right[1], draw='black!70', line_width='very thick')
    Connection.connect(box_spi_2.input_right[0].add_x(1.5), box_spi_2.input_right[0], text='Feedback',
                       text_position='start', line_width='very thick')

    box_spi_3 = Box(box_loop_controller.output_right[1].add(2.5, -1.5), size=(1.2, 1.2), fill='black', text='SPI\nDriver',
                    text_configuration=dict(text_color='white'), inputs=dict(left=1), outputs=dict(right=1))
    Connection.connect(box_loop_controller.output_right[1], box_spi_3.input_left[0], draw='black!70',
                       text=Text('$u(t)$'), move_text=(-0.2, 0.8), line_width='very thick')
    Connection.connect(box_spi_3.output_right[0], box_spi_3.output_right[0].add_x(1.5), text='Output',
                       text_position='end', line_width='very thick')

    # Save the document
    doc.save('pdf')

    # Show the document in the PDF Viewer
    doc.show()
