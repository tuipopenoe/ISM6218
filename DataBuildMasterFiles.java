// The GUI Frame for Master Files
import java.awt.*;
import javax.swing.*;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.URL;

public class DataBuildMasterFiles extends JFrame implements ActionListener{

    static final private String PLAY = "play";
    static final private String LAST = "last";
    static final private String ADD = "add";
    static final private String SUBTRACT = "subtract";

    public static void main(String[] args){
        SwingUtilities.invokeLater(new Runnable(){
            @Override
            public void run(){
                DataBuildMasterFiles master_files = new DataBuildMasterFiles();
                master_files.setVisible(true);
            }
        });
    }

    // Constructor
    public DataBuildMasterFiles(){
        init_UI();
    }

    private void init_UI(){
        JPanel pane = (JPanel) getContentPane();
        GroupLayout group_layout = new GroupLayout(pane);
        // Add content
        pane.setLayout(group_layout);
        pane.setToolTipText("Master Files");
        // Create the toolbar
        JToolBar tool_bar = new JToolBar("Master Files");
        this.add_buttons(tool_bar);
        // Create the text area
        JTextArea text_area = new JTextArea(5, 15);
        text_area.setEditable(false);
        JScrollPane scroll_pane = new JScrollPane(text_area);
        // Create Key length
        JLabel key_length = new JLabel("Key Length");
        JTextArea key_length_entry = new JTextArea();
        // Create Relative Key Postion 
        JLabel relative_key_position = new JLabel("Relative Key Position");
        JTextArea key_position_entry = new JTextArea(1, 10);
        group_layout.setAutoCreateContainerGaps(true);
        group_layout.setHorizontalGroup(group_layout.createSequentialGroup()
            .addGroup(group_layout.createParallelGroup()
                .addComponent(tool_bar)
                .addComponent(text_area)
                .addGap(200)
            )
            .addGroup(group_layout.createParallelGroup()
                .addComponent(relative_key_position)
                .addComponent(key_position_entry)
                .addGap(200)
                )
        );
        group_layout.setVerticalGroup(group_layout.createSequentialGroup()
            .addGroup(group_layout.createParallelGroup()
                .addComponent(tool_bar)
                .addComponent(text_area)
                .addGap(120)
            )
            .addGroup(group_layout.createParallelGroup()
                .addComponent(relative_key_position)
                .addComponent(key_position_entry)
                .addGap(120)
            )
        );

        pack();

        // Set the Frame title, size, relative location and default close
        setTitle("Master Files 1.0");
        setSize(640, 480);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

    protected void add_buttons(JToolBar tool_bar){
        JButton button = null;

        //play button
        button = make_button("play", PLAY,
                                      "Play",
                                      "Play");
        tool_bar.add(button);

        //last button
        button = make_button("last", LAST,
                                      "Last",
                                      "Last");
        tool_bar.add(button);

        //add button
        button = make_button("add", ADD,
                                      "Add",
                                      "Add");
        tool_bar.add(button);

        //subtract button
        button = make_button("subtract",
                             SUBTRACT,
                             "Subtract",
                             "Subtract");
        tool_bar.add(button);
    }

    protected JButton make_button(String image_name,
                                  String action_command,
                                  String tool_tip_text,
                                  String alt_text){
       //Look for the image.
        String image_location = "images/" + image_name + ".gif";
        URL image_url = DataBuildMasterFiles.class.getResource(image_location);

        //Create and initialize the button.
        JButton button = new JButton();
        button.setActionCommand(action_command);
        button.setToolTipText(tool_tip_text);
        button.addActionListener(this);

        if (image_url != null){
            button.setIcon(new ImageIcon(image_url, alt_text));
        }
        else {
            button.setText(alt_text);
            System.err.println("Resource not found: " + image_location);
        }

        return button;
    }

    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        // Handle each button.
        if (PLAY.equals(cmd)){
            // TODO: Play button
        }
        else if(LAST.equals(cmd)){
            // TODO: Last button 
        }
        else if(ADD.equals(cmd)){
            // TODO: subtract button
        }
        else if(SUBTRACT.equals(cmd)){
            // TODO: Subtract button
        }
    }
}