// This is the GUI for the DataBuild application
// It imports the DataBuild backend java for CRUD operations
// and creates a GUI that is linked to those operations
// GUI Components
import java.awt.*;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import javax.swing.border.LineBorder;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.SwingUtilities;
import javax.swing.plaf.metal.MetalIconFactory;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import javax.swing.border.TitledBorder;

import java.net.URL;

// DataBuild Access
//import DataBuild.*;

class DataBuildGUI extends JFrame implements ActionListener{
    protected static DataBuildGUI root_frame;
    public static void main(String[] args){
        Runnable r = new Runnable(){
            public void run(){
                DataBuildGUI data_build_gui = new DataBuildGUI();
                root_frame = data_build_gui;
                data_build_gui.setVisible(true);
            }
        };
        SwingUtilities.invokeLater(r);
    }

    // Constructor for the DataBuild GUI frame
    public DataBuildGUI(){
        init_UI();
    }

    protected void init_UI(){
        // Initialize the GUI main Panel
        final JPanel gui = new JPanel(new BorderLayout(5,5));
        gui.setBorder(new LineBorder(Color.BLACK, 1, false));

        // Create the menu bar
        final JMenuBar menu_bar = new JMenuBar();
        initialize_menu_bar(menu_bar);
        this.setJMenuBar(menu_bar);

        // Create the ToolBar
        final JPanel tool_bar_panel = new JPanel(
            new FlowLayout(FlowLayout.LEFT, 3, 3));
        JToolBar tool_bar = new JToolBar();
        // Add the buttons to the toolbar
        add_toolbar_buttons(tool_bar, this);
        // Add the tool bar object to the tool bar panel
        tool_bar_panel.add(tool_bar);
        // Place the tool bar in the Nort of the GUI
        gui.add(tool_bar_panel, BorderLayout.NORTH);


        // Labels layout
        JPanel dynamic_labels = new JPanel(new BorderLayout(4,4));
        dynamic_labels.setBorder(
            new LineBorder(Color.BLACK, 1, false));
        gui.add(dynamic_labels, BorderLayout.WEST);

        final JPanel labels = new JPanel(new GridLayout(0,2,3,3));
        labels.setBorder(
            new LineBorder(Color.BLACK, 1, false));

        JButton add_new = new JButton("Add Another Label");
        dynamic_labels.add(add_new, BorderLayout.NORTH);
        add_new.addActionListener(new ActionListener(){
            private int label_count = 0;
            public void actionPerformed(ActionEvent e){
                labels.add(new JLabel("Label" + ++label_count));
                gui.validate();
            }
        });

        dynamic_labels.add(new JScrollPane(labels),
            BorderLayout.CENTER);


        // Table Layout
        String[] header = {"Name", "Value"};
        String[] a = new String[0];
        String[] names = System.getProperties().
            stringPropertyNames().toArray(a);
        String[][] data = new String[names.length][2];
        for(int i=0; i < names.length; i++){
            data[i][0] = names[i];
            data[i][1] = System.getProperty(names[i]);
        }
        DefaultTableModel model = new DefaultTableModel(data, header);
        JTable table = new JTable(model);
        try{
            table.setAutoCreateRowSorter(true);
        }
        catch(Exception continuewithNoSort){

        }
        JScrollPane table_scroll = new JScrollPane(table);
        Dimension table_preferred = table_scroll.getPreferredSize();
        table_scroll.setPreferredSize(
            new Dimension(table_preferred.width,
                table_preferred.height));

        // Image pane layout
        JPanel image_panel = new JPanel(new GridBagLayout());
        image_panel.setBorder(
            new LineBorder(Color.BLACK, 1, false));


        // Split the table and the image panel 
        JSplitPane split_pane = new JSplitPane(
            JSplitPane.VERTICAL_SPLIT,
            table_scroll,
            new JScrollPane(image_panel));
        // Add the Split pane to the center and east portions
        gui.add(split_pane, BorderLayout.CENTER);


        // Initialize the root data build frame
        this.setContentPane(gui);
        this.pack();
        this.setLocationRelativeTo(null);
        this.setTitle("DataBuild Version 1.0");
        this.setSize(1280, 720);
        try{
            this.setLocationByPlatform(true);
            this.setMinimumSize(this.getSize());
        }
        catch(Throwable ignoreAndContinue){

        }
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);
    }

    protected static void initialize_menu_bar(JMenuBar menu_bar){
        // File Menu
        JMenu file_menu = new JMenu("File");
        file_menu.setMnemonic(KeyEvent.VK_F);

        JMenuItem exit_menu_item = new JMenuItem("Exit");
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
    protected static void add_toolbar_buttons(JToolBar tool_bar,
                                              DataBuildGUI data_build_gui){
        // Button placeholder
        JButton button = null;

        // Master Files button
        button = make_button("master_files",
                             "Open Master Files Pane",
                             "Master Files",
                             data_build_gui);
        tool_bar.add(button);

        // Relationships button
        button = make_button("relationships",
                             "Open Relationships Pane",
                             "Relationships",
                             data_build_gui);
        tool_bar.add(button);

        // Views button
        button = make_button("views",
                             "Open Views Pane",
                             "Views",
                             data_build_gui);
        tool_bar.add(button);

        // Generate button
        button = make_button("generate",
                             "Open Generate Pane",
                             "Generate",
                             data_build_gui);
        tool_bar.add(button);

        // View Log button
        button = make_button("view_log",
                             "Open the View Log Pane",
                             "View Log",
                             data_build_gui);
        tool_bar.add(button);
    }

    // Create a new button 
    protected static JButton make_button(String action_command,
                                         String tool_tip_text,
                                         String alt_text,
                                         DataBuildGUI data_build_gui)
    {
        // Create and initialize the button
        JButton button = new JButton(alt_text);
        button.setActionCommand(action_command);
        button.setToolTipText(tool_tip_text);
        button.addActionListener(data_build_gui);

        return button;
    }

    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        // Handle each button.
        if ("master_files".equals(cmd)){
            SwingUtilities.invokeLater(new Runnable(){
                @Override
                public void run(){
                    DataBuildMasterFiles mf = new DataBuildMasterFiles();
                    mf.setLocationRelativeTo(root_frame);
                    mf.setVisible(true);
                }
            });
        }
        else if ("relationsips".equals(cmd)){
            //TODO: Open Relationships Pane
        }
        else if ("views".equals(cmd)){
            //TODO: Open VIEWS pane
        }
        else if("generate".equals(cmd)){
            //TODO: Open Generate Pane
        }
        else if("view_log".equals(cmd)){
            //TODO: Open View Log pane
        }
    }
}
