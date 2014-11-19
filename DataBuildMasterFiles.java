// The GUI Frame for Master Files
import java.awt.*;
import javax.swing.*;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.URL;

public class DataBuildMasterFiles extends JPanel implements ActionListener{

    protected JTextArea text_area;
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
        super(new BorderLayout());

        // Create the toolbar
        JToolBar tool_bar = new JToolBar("Master Files");
        add_buttons(tool_bar);

        // Create the text area
        text_area = new JTextArea(5, 30);
        text_area.setEditable(false);
        JScrollPane scroll_pane = new JScrollPane(text_area);

        // Layout the main panel
        setPreferredSize(new Dimension(640, 480));
        add(tool_bar, BorderLayout.PAGE_START);
        add(scroll_pane, BorderLayout.CENTER);
    }

    private static void init_UI(){
        JFrame frame = new JFrame("Master Files");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        // Add content
        frame.add(new DataBuildMasterFiles());

        // Display the window
        frame.pack();
        frame.setVisible(true);
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