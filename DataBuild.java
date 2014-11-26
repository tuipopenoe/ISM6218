// DataBuild CRUD application
// To Execute, run MySQL with localhost open on port 1337
// DataBuild will execute the initialize table sql script in the same directory
// GUI elements can be found in the DataBuild_GUI class.
// TODO: Finish unit tests


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;
import java.sql.SQLException;

import java.io.*;

class DataBuild{
    // Class variables
    private String url;
    private String password;
    private String login;
    private String input;

    private Connection connection;

    // Constructor
    public void DataBuild(){
        // Initialize the DB connection
        /*this.connection = create_connection("jdbc:mysql://localhost:1337/init",
            "username", "passw0rd");*/

    }

    public static void main(String[] args){
        // Open Standard input
        BufferedReader b = new BufferedReader(new InputStreamReader(System.in));
        try{
            // Create the connection with the initial command line arguments
            DataBuild data_build = new DataBuild();
            // Open the connection to the database
            data_build.establish_connection(b);
            data_build.execute_input(b);
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
    }

    protected void init_default_login(){
        // Initialize the default url and login credentials
        this.set_url("jdbc:mysql://localhost:3306/testdb");
        this.set_login("root");
        this.set_password("passw0rd");
    }

    protected void establish_connection(BufferedReader br){
        try{
            System.out.println("Enter the url to connect to: ");
            System.out.print(">> ");
            this.set_input(br.readLine());
            System.out.println(this.get_input());
            if(this.get_input().isEmpty()){
                // Default URL
                this.set_url("jdbc:mysql://localhost:3306/testdb");
            }
            this.set_url(this.get_input());
            System.out.println(this.get_url());
            System.out.println("\nEnter the login for the database: ");
            System.out.print(">> ");
            this.set_input(br.readLine());
            // Default Login
            if(this.get_input().isEmpty()){
                this.set_login("root");
            }
            this.set_login(this.get_input());
            System.out.println("\nEnter the password for the database: ");
            System.out.print(">> ");
            this.set_input(br.readLine());
            // Default Password
            if(this.get_input().isEmpty()){
                this.set_password("passw0rd");
            }
            this.set_password(this.get_input());
            System.out.println("\nEstablishing Connection...");
            this.set_connection(DriverManager.getConnection(get_url(),
                get_login(), get_password()));
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
        System.out.println("\nConnected");
    }

    protected void execute_input(BufferedReader br){
        boolean exit = false;
        while(!exit){
            try{
                // Prompt the User
                System.out.print(">>: ");
                // Set the input to the entered command
                this.set_input(br.readLine());
                // exit the program
                if(this.get_input().equals("exit")){
                    exit = true;
                    break;
                }
                // display the program version
                else if(this.get_input().equals("version")){
                    Connection con = this.get_connection();
                    Statement st = con.createStatement();
                    ResultSet rs = st.executeQuery("SELECT VERSION");
                    if(rs.next()){
                        System.out.println(rs.getString(1));
                    }
                }
            }
            catch(Exception e){

            }
        }
    }

    // Accessors and Mutators
    public String get_input(){
        return this.input;
    }

    public void set_input(String input){
        this.input = input;
    }

    public String get_url(){
        return this.url;
    }

    public void set_url(String url){
        this.url = url;
    }

    public String get_login(){
        return this.login;
    }

    public void set_login(String login){
        this.login = login;
    }

    public String get_password(){
        return this.password;
    }

    public void set_password(String password){
        this.password = password;
    }


    public Connection get_connection(){
        return this.connection;
    }

    public void set_connection(Connection connection){
        this.connection = connection;
    }

    // Initialize Table
    public boolean initialize_table(){
        try{
            execute_command("/initialize_table.sql");
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
        // Execute the sql script initialize_table.sql
        return false;
    }

    public void execute_command(String command){
        try{
            // Get the current runtime
            Runtime rt = Runtime.getRuntime();
            // Get the current working directory
            String path = new File("").getAbsolutePath();
            // Execute command in the current directory
            Process pr = rt.exec(path + command);
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
    }

    // Create Connection
    // Return the connection object
    public Connection create_connection(String dbURL, String username,
        String password){
        try{
            // Check if the mysql service is running
            //execute_command
            // Start the mysql service
            Connection conn = (Connection) DriverManager.getConnection(
                dbURL, username, password);
            if (conn != null){
                System.out.println("Connected");
                return conn;
            }
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
        return null;
    }

    // Select Insert Update Delete
    public boolean select(String[] columns, String table){
        try{
            // Create a select all from the table
            String sql = "SELECT * FROM " + table;
            // Create the statement over the connection
            Statement statement = this.connection.createStatement();
            // Execute the SELECT
            ResultSet result_set = statement.executeQuery(sql);
            ResultSetMetaData meta = result_set.getMetaData();
            int number_of_columns = meta.getColumnCount();

            int count = 0;

            // The select used is static so the next() method moves the cursor
            // forward in the result set to check if there is another record
            // If a record exists, print the values of that record.
            // Take note, the column index is 1-based, not 0-based.
            while(result_set.next()){
                String record_number = result_set.getString(1);
                String primary_key = result_set.getString(2);
                System.out.print("Primary Key: ");
                for(int i = 1; i <= number_of_columns -1; i++){
                    System.out.print(result_set.getString(i) + "\t");
                }
                System.out.print("\n");
            }
            // Command executed successfully
            return true;
        }
        catch(Exception ex){
            // Command failed
            return false;
        }
    }

    public boolean insert(String[] columns, String[] values, String table){
        try{
            // Check the column length and value length matches
            if(columns.length != values.length){
                System.out.println("ERROR: Invalid number of columns/values");
            }
            String sql = "INSERT INTO " + table + "(";
            String placeholders = "(";
            // Append the column names and the placeholders
            // Creates a statement in the form:
            // "INSERT INTO <table> (col1, col2, col3) VALUES (?, ?, ?)"
            for(int i = 0; i < columns.length - 1; i++){
                if(i != columns.length - 1){
                    sql += columns[i] + ",";
                    placeholders += "?, ";
                }
                else{
                    sql += columns[i] + ")";
                    placeholders += "?)";
                }
            }
            // Attach the VALUES instruction
            sql += " VALUES " + placeholders;
            // Create the statement
            PreparedStatement statement = this.connection.prepareStatement(sql);
            // And replace the placeholder (?) in the statement with values[]
            for(int j = 0; j < values.length -1; j++){
                statement.setString(j, values[j]);
            }
            // Execute the insert statement and get the number of rows inserted
            int rows_inserted = statement.executeUpdate();
            if(rows_inserted > 0){
                System.out.println("A new record was inserted successfully!");
            }
            return true;
        }
        catch(Exception ex){
            ex.printStackTrace();
            return false;
        }
    }

    public boolean update(String[] columns, String[] values, String table){
        try{
            // Initialize the update statement
            String sql = "UPDATE " + table + " SET ";
            // Add in the column placeholders
            for(int i = 0; i < columns.length; i++){
                if(i != columns.length - 1){
                    sql += (columns[i] + "=?,");
                }
                else{
                    sql += (columns[i] + "=?");
                }
            }
            // Create the sql statement
            PreparedStatement statement = this.connection.prepareStatement(sql);
            // Replace the sql statement with values from values[]
            for(int j = 1; j < values.length; j++){
                statement.setString(j, values[j-1]);
            }
            // Execute the update command
            int rows_updated = statement.executeUpdate();
            if(rows_updated > 0){
                System.out.println("An existing record was updated succesfully");
            }
            // Command executed Successfully!
            return true;
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
        return false;
    }

    public boolean delete(String table, String column, String value){
        try{
            // Initialiez the DELETE command
            String sql = "DELETE FROM " + table + " WHERE " + column + "=?";
            // Create the sql command statement
            PreparedStatement statement  = this.connection.prepareStatement(sql);
            // Replace the placeholder with the value to select to delete
            statement.setString(1, value);
            // Execute the DELETE command and get the number of rows deleted
            int rows_deleted = statement.executeUpdate();
            if(rows_deleted > 0){
                System.out.println("A record was deleted successfully!");
            }
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
        return false;
    }

/*    // Main Method
    public static void main(String[] args){
        try{
            // Create the connection with the initial command line arguments
            DataBuild data_build = new DataBuild();
            data_build.unit_tests();
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
    }
*/
    public boolean unit_tests(){
        try{
            // Tests executed succesfully
            System.out.println("Tests Executed Successfully");
            return true;
        }
        catch(Exception ex){
            ex.printStackTrace();
        }
        return false;
    }
}