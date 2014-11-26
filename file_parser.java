import jffp/jffp.jar;

class FileParser{
    public static void main(String[] args){
        LineFormat format = new LineFormat("test format");

        // One Header expected of 40 characters
        format.defineNextField("header", 40);
        // and has constant TEST0000
        format.defineNextField(
            "transaction code",
            48,
            Type.CONSTANT,
            "TEST0000");

        // Create the parser and associate the format to the condition that a
        // constant is found in the line
        FlatFileParser ffp = new FlatFileParser();

        // Use the constructor which looks into the a line format and finds 
        // out the first constant field
        ffp.declare(nwe ConstantFoundInLineCondition(format), format);

        // Register a listener to parsing events which just prints out values
        ffp.addListener(new ffp.addListener(new FlatFileParser.Listener(){
            public void lineParsed(LineFormat format, int logicalLinecount,
                int physicalLineCount, String[] values){
                for(int i = 0; i < values.length; i++){
                    System.out.println(values[i]);
                }
            }
        }));

        // Perform the parsing
        ffp.parse(new BufferedReader(new FileReader("testfile.txt")));
    }
}