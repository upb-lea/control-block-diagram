from control_block_diagram import ControllerDiagram
from control_block_diagram.components import Box, Connection, Point, Circle
from control_block_diagram.predefined_components import Add


if __name__ == '__main__':

    # Initialize a new block diagram
    doc = ControllerDiagram()

    # Add components to the document
    box_inp = Box(Point(0, 0), size=(1.5, 0.8), text=r'$R_{\mathrm{r}} \frac{L_{\mathrm{m}}}{L_{\mathrm{r}}}$')
    Connection.connect(box_inp.input_left[0].sub_x(1), box_inp.input_left[0], text=r'$\underline{i}_{\mathrm{s}}$',
                       text_position='start', text_align='top', distance_y=0.3)

    add = Add(box_inp.output_right[0].add_x(1.5))
    Connection.connect(box_inp.output_right, add.input_left)

    box_int = Box(add.output_right[0].add_x(1.5), size=(1, 0.8), text=r'$\frac{1}{s}$')
    Connection.connect(add.output_right, box_int.input_left)
    Connection.connect(box_int.output_right[0], box_int.output_right[0].add_x(2),
                       text=r'$\underline{\Psi}_{\mathrm{r}}$', distance_y=0.3)

    box_back = Box(box_int.position.sub_y(1.5), size=(1.8, 0.8),
                   text=r'$\frac{R_{\mathrm{r}}}{L_{\mathrm{r}}}-\mathrm{j} \omega_{\mathrm{rs}}$')
    con = Connection.connect(box_int.output_right[0].add_x(1), box_back.output_right[0], start_direction='south')

    Circle(con.start, radius=0.05, fill='black')
    Connection.connect(box_back.input_left, add.input_bottom, text='-', text_position='end', text_align='right',
                       move_text=(-0.2, -0.2))

    # Save the document
    doc.save('pdf', 'tex')

    # Show the document in the PDF Viewer
    doc.show()
