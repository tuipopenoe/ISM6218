// The GUI Frame for Master Files
import java.awt.*;
import javax.swing.*;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.URL;
import javax.swing.border.LineBorder;
import javax.swing.border.TitledBorder;

public class DataBuildMasterFiles extends JFrame implements ActionListener{

    static final private String PLAY = "play";
    static final private String LAST = "last";
    static final private String ADD = "add";
    static final private String SUBTRACT = "subtract";

    public static void main(String[] args){
        Runnable r = new Runnable(){
            @Override
            public void run(){
                DataBuildMasterFiles master_files = new DataBuildMasterFiles();
                master_files.setVisible(true);
            }
        };
        SwingUtilities.invokeLater(r);
    }

    // Constructor
    public DataBuildMasterFiles(){
        init_UI();
    }

    private void init_UI(){
        // Initialize the GUI
        JPanel master_files_gui = new JPanel(new BorderLayout(5, 5));
        master_files_gui.setBorder(new LineBorder(Color.BLACK, 1, false));
        master_files_gui.setToolTipText("Master Files");

        // Create the toolbar
        final JPanel tool_bar_panel = new JPanel(
            new FlowLayout(FlowLayout.LEFT, 3, 3));
        JToolBar tool_bar = new JToolBar();
        this.add_buttons(tool_bar);
        tool_bar_panel.add(tool_bar);
        master_files_gui.add(tool_bar_panel, BorderLayout.NORTH);

        // Create the text area
        JPanel text_area_panel = new JPanel(new BorderLayout(4,4));
        text_area_panel.setBorder(
            new LineBorder(Color.BLACK, 1, false));

        JTextArea text_area = new JTextArea(15, 18);
        text_area.setEditable(false);
        JScrollPane scroll_pane = new JScrollPane(text_area);

        text_area_panel.add(text_area, BorderLayout.NORTH);
        master_files_gui.add(text_area_panel, BorderLayout.WEST);



        // Create Key length
        JPanel key_panel = new JPanel(new BorderLayout(5,5));
        key_panel.setBorder(new TitledBorder(""));
        JLabel key_length = new JLabel("Key Length: ");
        JTextArea key_length_entry = new JTextArea(1, 20);
        key_panel.add(key_length, BorderLayout.CENTER);
        key_panel.add(key_length_entry, BorderLayout.EAST);

        // Create Relative Key Postion
        JPanel position_panel = new JPanel(new BorderLayout(5,5));
        position_panel.setBorder(new TitledBorder(""));
        JLabel relative_key_position = new JLabel("Relative Key Position");
        JTextArea key_position_entry = new JTextArea(1, 20);
        position_panel.add(relative_key_position, BorderLayout.WEST);
        position_panel.add(key_position_entry, BorderLayout.EAST);

        // File Type Panel
        JPanel file_type_panel = new JPanel(new GridLayout(0, 1));
        file_type_panel.setBorder(new TitledBorder("File Type"));
        JRadioButton seq_button = new JRadioButton("Sequential");
        JRadioButton ksds_button = new JRadioButton("VSAM Key Sequence Dataset(KSDS)");
        JRadioButton rrds_button = new JRadioButton("VSAM Relative Record Dataset (RRDS)");
        JRadioButton esds_button = new JRadioButton("VSAM Entry Sequenced Dataset (ESDS)");
        ButtonGroup button_group = new ButtonGroup();
        button_group.add(seq_button);
        button_group.add(ksds_button);
        button_group.add(rrds_button);
        button_group.add(esds_button);
        file_type_panel.add(seq_button);
        file_type_panel.add(ksds_button);
        file_type_panel.add(rrds_button);
        file_type_panel.add(esds_button);

        // Entry Panel
        JPanel entry_panel = new JPanel(new BorderLayout(0,0));
        entry_panel.setBorder(new LineBorder(Color.BLACK, 0, false));
        entry_panel.add(key_panel, BorderLayout.NORTH);
        entry_panel.add(position_panel, BorderLayout.CENTER);
        entry_panel.add(file_type_panel, BorderLayout.SOUTH);




        // Description Panel
        JPanel description_panel = new JPanel(new BorderLayout(5,5));
        JPanel description_text_panel = new JPanel(new BorderLayout(0, 0));
        description_text_panel.setBorder(new TitledBorder("Description: "));
        JTextArea description = new JTextArea(10, 15);
        description_text_panel.add(description);

        // DDName
        JPanel ddname_panel = new JPanel(new BorderLayout(0,0));
        ddname_panel.setBorder(new TitledBorder(""));
        JLabel ddname_label = new JLabel("DDName: ");
        JTextArea ddname_text_area = new JTextArea(1, 15);
        ddname_panel.add(ddname_label, BorderLayout.WEST);
        ddname_panel.add(ddname_text_area, BorderLayout.EAST);

        description_panel.add(ddname_panel, BorderLayout.NORTH);
        description_panel.add(description_text_panel, BorderLayout.CENTER);

        // Right Panel
        JPanel right_panel = new JPanel(new BorderLayout(5, 5));
        right_panel.setBorder(new TitledBorder(""));
        right_panel.add(entry_panel, BorderLayout.NORTH);
        right_panel.add(description_panel, BorderLayout.CENTER);

        master_files_gui.add(right_panel, BorderLayout.CENTER);

        // Initialize the master files frame
        this.setContentPane(master_files_gui);
        pack();
        // Set the Frame title, size, relative location and default close
        setTitle("Master Files 1.0");
        setSize(720, 640);
        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
    }

    protected void add_buttons(JToolBar tool_bar){
        JButton button = null;

        //play button
        button = make_button("play",
                             "Play",
                             "Play");
        tool_bar.add(button);

        //last button
        button = make_button("last",
                             "Last",
                             "Last");
        tool_bar.add(button);

        //add button
        button = make_button("add",
                             "Add",
                             "Add");
        tool_bar.add(button);

        //subtract button
        button = make_button("subtract",
                             "Subtract",
                             "Subtract");
        tool_bar.add(button);
    }

    protected JButton make_button(String action_command,
                                  String tool_tip_text,
                                  String alt_text){
        //Create and initialize the button.
        JButton button = new JButton(alt_text);
        button.setActionCommand(action_command);
        button.setToolTipText(tool_tip_text);
        button.addActionListener(this);
        return button;
    }

    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        // Handle each button.
        if ("play".equals(cmd)){
            // TODO: Play button
        }
        else if("last".equals(cmd)){
            // TODO: Last button 
        }
        else if("add".equals(cmd)){
            // TODO: subtract button
        }
        else if("subtract".equals(cmd)){
            // TODO: Subtract button
        }
    }
}