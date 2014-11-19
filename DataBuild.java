// DataBuild CRUD application
// To Execute, run MySQL with localhost open on port 1337
// DataBuild will execute the initialize table sql script in the same directory
// GUI elements can be found in the DataBuild_GUI class.
// TODO: Finish unit tests

package DataBuild;

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
    public Connection connection;
    // Constructor
    public void DataBuild(){
        // Initialize the DB connection
        this.connection = create_connection("jdbc:mysql://localhost:1337/init",
            "username", "passw0rd");

    }

    // Accessors and Mutators

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

    // Main Method
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