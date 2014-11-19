// This is the GUI for the DataBuild application
// It imports the DataBuild backend java for CRUD operations
// and creates a GUI that is linked to those operations
// GUI Components
import java.awt.*;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.SwingUtilities;
import javax.swing.plaf.metal.MetalIconFactory;

import java.net.URL;

// DataBuild Access
//import DataBuild.*;

public class DataBuildGUI extends JFrame implements ActionListener{


    static final private String MASTER_FILES = "master_files";
    static final private String RELATIONSHIPS = "relationships";
    static final private String VIEWS = "views";
    static final private String GENERATE = "generate";
    static final private String VIEW_LOG = "view_log";

    public static void main(String[] args){
        // Places the application on the Swing Event Queue
        // Ensures that all UI updates are concurrency-safe (prevent hanging)
        SwingUtilities.invokeLater(new Runnable(){
            @Override
            public void run(){
                // Create the GUI and display it to the screen
                DataBuildGUI data_build_gui = new DataBuildGUI();
                data_build_gui.setVisible(true);
            }
        });
    }
    // Constructor
    public DataBuildGUI(){
        init_UI();
    }

    private void init_UI(){
        // Set the content pane of the JFrame where the child components are 
        // placed. Organize the child components with the GroupLayout 
        // layout manager
        JPanel pane = (JPanel) getContentPane();
        GroupLayout group_layout = new GroupLayout(pane);
        pane.setLayout(group_layout);

        // Set Tooltip for the pane
        pane.setToolTipText("DataBuild Application Version 1.0");

        //######################################################################
        // DataBuild Components
        //######################################################################

        // DataBuild Menus
        //######################################################################
        JMenuBar menu_bar = new JMenuBar();
        // Intiliaze the menu bar
        this.initialize_menu_bar(menu_bar);

        // Set the frame's menu to menu_bar
        setJMenuBar(menu_bar);

        // DataBuild Toolbar
        //######################################################################
        JToolBar tool_bar = new JToolBar("DataBuild ToolBar");
        // Initialize the toolbar
        this.add_toolbar_buttons(tool_bar);

        // Child Frames:


        // Status Bar
        // #####################################################################
        /*JLabel status_label = new JLabel("status");
        status_label.setHorizontalAlignment(SwingConstants.LEFT);
        */
        // Initialize the Group Layout
        // Creates gaps between the components and the edges of the container
        group_layout.setAutoCreateContainerGaps(true);

        // Add Components to group Layout
        group_layout.setHorizontalGroup(group_layout.createSequentialGroup()
            // Add the component 
            .addComponent(tool_bar)
            // Add specific gap
            .addGap(200)
        );

        group_layout.setVerticalGroup(group_layout.createSequentialGroup()
            .addComponent(tool_bar)
            .addGap(120)
        );

        // Pack the components in the layout for rendering
        // Automatically sizes the JFrame based on the size of the components
        pack();

        // Set the Frame title, size, relative location and default close
        setTitle("DataBuild 1.0");
        setSize(1280, 720);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
    }

    protected void initialize_menu_bar(JMenuBar menu_bar){
        // Initialize Icons
        ImageIcon exit_icon = new ImageIcon("exit.png");

        // File Menu
        JMenu file_menu = new JMenu("File");
        file_menu.setMnemonic(KeyEvent.VK_F);

        JMenuItem exit_menu_item = new JMenuItem("Exit", exit_icon);
        exit_menu_item.setMnemonic(KeyEvent.VK_X);
        exit_menu_item.setToolTipText("Exit Application");
        exit_menu_item.addActionListener(new ActionListener(){
            @Override
            public void actionPerformed(ActionEvent event){
                System.exit(0);
            }
        });
        // Add items to File Menu
        file_menu.add(exit_menu_item);

        // Edit Menu
        JMenu edit_menu = new JMenu("Edit");
        edit_menu.setMnemonic(KeyEvent.VK_E);
        // TODO: Add menu items

        // View Menu
        JMenu view_menu = new JMenu("View");
        view_menu.setMnemonic(KeyEvent.VK_V);
        // TODO: Add menu items

        // Options Menu
        JMenu options_menu = new JMenu("Options");
        options_menu.setMnemonic(KeyEvent.VK_O);
        // TODO: Add menu items

        // Tools Menu
        JMenu tools_menu = new JMenu("Tools");
        tools_menu.setMnemonic(KeyEvent.VK_T);
        // TODO: Add menu items

        // Window Menu
        JMenu window_menu = new JMenu("Window");
        window_menu.setMnemonic(KeyEvent.VK_W);
        // TODO: Add menu items

        // Help Menu
        JMenu help_menu = new JMenu("Help");
        help_menu.setMnemonic(KeyEvent.VK_H);


        // Add menus to menu bar
        menu_bar.add(file_menu);
        menu_bar.add(edit_menu);
        menu_bar.add(view_menu);
        menu_bar.add(options_menu);
        menu_bar.add(tools_menu);
        menu_bar.add(window_menu);
        menu_bar.add(help_menu);
    }

    // Toolbar button methods
    // #########################################################################
    // Add button to the selected tool bar
    protected void add_toolbar_buttons(JToolBar tool_bar){
        // Button placeholder
        JButton button = null;

        // Master Files button
        button = make_toolbar_button("master_files",
                                     MASTER_FILES,
                                     "Open Master Files Pane",
                                     "Master Files");
        tool_bar.add(button);

        // Relationships button
        button = make_toolbar_button("relationships",
                                     RELATIONSHIPS,
                                     "Open Relationships Pane",
                                     "Relationships");
        tool_bar.add(button);

        // Views button
        button = make_toolbar_button("views",
                                     VIEWS,
                                     "Open Views Pane",
                                     "Views");
        tool_bar.add(button);

        // Generate button
        button = make_toolbar_button("generate",
                                     GENERATE,
                                     "Open Generate Pane",
                                     "Generate");
        tool_bar.add(button);

        // View Log button
        button = make_toolbar_button("view_log",
                                     VIEW_LOG,
                                     "Open the View Log Pane",
                                     "View Log");
        tool_bar.add(button);
    }

    // Create a new button 
    protected JButton make_toolbar_button(String image_name,
                                          String action_command,
                                          String tool_tip_text,
                                          String alt_text)
    {
        // Look for the image
        String image_location = "images/" + image_name + ".png";
        URL image_url = DataBuildGUI.class.getResource(image_location);

        // Create and initialize the button
        JButton button = new JButton();
        button.setActionCommand(action_command);
        button.setToolTipText(tool_tip_text);
        button.addActionListener(this);

        // Check if the image exists
        if(image_url != null){
            // Image found
            button.setIcon(new ImageIcon(image_url, alt_text));
        }
        else{
            // Image not found
            button.setText(alt_text);
            System.err.println("Resource not found: "+ image_location);
        }

        return button;
    }

    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        // Handle each button.
        if (MASTER_FILES.equals(cmd)){
            //TODO: Open Master Files Pane
        }
        else if (RELATIONSHIPS.equals(cmd)){
            //TODO: Open Relationships Pane
        }
        else if (VIEWS.equals(cmd)){
            //TODO: Open VIEWS pane
        }
        else if(GENERATE.equals(cmd)){
            //TODO: Open Generate Pane
        }
        else if(VIEW_LOG.equals(cmd)){
            //TODO: Open View Log pane
        }
    }
}

/*class DataBuildMasterFiles extends JFrame{

}*/