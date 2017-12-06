import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.awt.image.BufferedImage;
import java.io.*;

/**
 * Created by samhollenbach on 2/15/16.
 */
public class SimReader extends JFrame implements KeyListener, MouseWheelListener {

    JFrame frame;
    int windowWidth;
    int windowHeight;
    boolean isRunning = true;
    boolean paused = false;
    final int fps = 60;
    File f;
    int particleNumber;
    BufferedReader br;
    BufferedImage backBuffer;
    boolean loop = true;
    double scale;
    double scalePow = 1;
    double scaleMin = 10;
    double scaleMax = 10;
    double readerX = 0;
    double readerY = 0;

    double scaleBar = 0;

    boolean saveMovie = true;
    boolean show_columns = false;

    public SimReader(File f){
        this.f = f;
    }


    public static void main(String[] args) {
        SimReader sr = new SimReader(new File("PedestrianData.csv"));
        sr.run();
    }

    void initializeReader(){
        try {
            br = new BufferedReader(new FileReader(f));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.out.println("Data file not found");
        }
    }

    void run(){
        initialize();
        setIgnoreRepaint(true);

        initializeReader();

        scale = Math.pow(10,scalePow);

        processHeading();

        startReading();


        setVisible(false);
        System.exit(0);
    }

    void startReading(){
        while(isRunning)
        {
            long time = System.currentTimeMillis();

            //  delay for each frame  -   time it took for one frame
            time = (1000 / fps) - (System.currentTimeMillis() - time);

            if(!paused){
                readIteration(br);
            }

            //System.out.println(time);
            if (time > 0)
            {
                try{
                    Thread.sleep(time);
                }catch(Exception e){}
            }
        }
    }


    void processHeading(){
        String heading = "";
        try {
            heading = br.readLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println(heading + " ");
        String[] heading_data = heading.split(",");
        particleNumber = Integer.valueOf(heading_data[1]);
        System.out.println(particleNumber);
    }

    void initialize(){
        frame = this;
        windowWidth = 900;
        windowHeight = 500;
        setTitle("Pedestrian Sim");
        setSize(windowWidth, windowHeight);
        setResizable(false);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);

        addKeyListener(this);
        addMouseWheelListener(this);

        backBuffer = new BufferedImage(windowWidth, windowHeight, BufferedImage.TYPE_INT_RGB);
    }

    /*
    * Reads file data for each iteration of the simulation.
    *
    *
    */
    void readIteration(BufferedReader br){
        Graphics g = getGraphics();
        Graphics2D bbg = (Graphics2D)backBuffer.getGraphics();

        bbg.setColor(Color.BLACK);
        bbg.fillRect(0,0,windowWidth,windowHeight);

        int[] topLeft = translateCoordinatesToScreen(-20,-20,0);
        int[] topRight = translateCoordinatesToScreen(20,-20,0);
        int[] botLeft = translateCoordinatesToScreen(-20,20,0);
        int[] botRight = translateCoordinatesToScreen(20,20,0);
        int[] gapLeft = translateCoordinatesToScreen(-1,20,0);
        int[] gapRight = translateCoordinatesToScreen(1,20,0);
        bbg.setColor(Color.WHITE);
        bbg.drawLine(topLeft[0], topLeft[1], topRight[0], topRight[1]);
        bbg.drawLine(topLeft[0], topLeft[1], botLeft[0], botLeft[1]);

        bbg.drawLine(botRight[0], botRight[1], topRight[0], topRight[1]);
        bbg.drawLine(gapLeft[0], gapLeft[1], botLeft[0], botLeft[1]);
        bbg.drawLine(botRight[0], botRight[1], gapRight[0], gapRight[1]);


        double currentIter = 0;



        int[] cl = translateCoordinatesToScreen(0,0,0);
        bbg.setColor(Color.RED);
        //bbg.fillOval(cl[0],cl[1],3*(int)scale,3*(int)scale);


        for(int i = 0; i < particleNumber; i++){



            String fileLine = null;
            try {
                if((fileLine = br.readLine()) == null){
                    if(loop){
                        saveMovie = false;
                        initializeReader();
                    }
                    return;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            String[] data = fileLine.split(",");
            Double[] numData = new Double[data.length];
            if (numData.length == 0) {
                return;
            }


            for(int j = 0; j < data.length; j++){
                int index = data[j].indexOf("=");
                numData[j] = Double.parseDouble(data[j].substring(index+1,data[j].length()));

            }
            if (numData[0] == -1){
                System.out.println(numData[2]);
                int[] col_loc = translateCoordinatesToScreen(numData[1], numData[2],0);
                System.out.println(numData[3].intValue());
                bbg.drawOval(col_loc[0],col_loc[1],numData[3].intValue(),numData[3].intValue());
                System.out.println(col_loc[1]);
                bbg.setColor(Color.RED);
                bbg.fillRect(col_loc[0]-2,col_loc[1]-2,col_loc[0]+2,col_loc[1]+2);
            }

            if (numData.length < 7){
                return;
            }

            if(numData[0] != currentIter){
                currentIter = numData[0];
            }
            //Gets location to draw
            int[] screenLocation = translateCoordinatesToScreen(numData[2],numData[3],0);

            int color = 0;
            bbg.setColor(Color.GREEN);



            //TODO: Probably changing to 3D at some point, but for now seen from above on Y axis, viewing X and Z axes
            //Also set at 1 pixel size particle right now, but can adjust for what looks best when closer to finished

            int ovalSize = numData[6].intValue();


            if(color == 0){
                bbg.fillOval(screenLocation[0],screenLocation[1],ovalSize*(int)scale,ovalSize*(int)scale);
                bbg.setColor(Color.WHITE);
                bbg.drawOval(screenLocation[0],screenLocation[1],ovalSize*(int)scale,ovalSize*(int)scale);
            }else{
                bbg.fillOval(screenLocation[0],screenLocation[1],ovalSize*(int)scale,ovalSize*(int)scale);
            }

            if(show_columns){
                bbg.setColor(Color.RED);
                int[] topLeft1 = translateCoordinatesToScreen(-12,-2,0);
                bbg.fillRect(topLeft1[0],topLeft1[1],4*(int)scale,4*(int)scale);

                int[] topLeft2 = translateCoordinatesToScreen(8,8,0);
                bbg.fillRect(topLeft2[0],topLeft2[1],4*(int)scale,4*(int)scale);

                int[] topLeft3 = translateCoordinatesToScreen(-12,8,0);
                bbg.fillRect(topLeft3[0],topLeft3[1],4*(int)scale,4*(int)scale);

                int[] topLeft4 = translateCoordinatesToScreen(8,-2,0);
                bbg.fillRect(topLeft4[0],topLeft4[1],4*(int)scale,4*(int)scale);

            }

        }
        String currentIterString = String.valueOf(currentIter);
        currentIterString = currentIterString.substring(0,currentIterString.indexOf("."));

        bbg.setColor(Color.WHITE);
        bbg.drawString(currentIterString,30,50);
        bbg.drawString("Maximum Occupancy: 40",30,70);
        bbg.setColor(Color.WHITE);

        g.drawImage(backBuffer, 0, 0, this);
        if(saveMovie){
            try {
                File outputFile = new File("frames/frame_"+currentIterString+".jpg");
                ImageIO.write(backBuffer,"jpg", outputFile);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        bbg.dispose();
        g.dispose();

    }

    //Takes the 3D coordinates of the particle and translates it to the simulation screen
    public int[] translateCoordinatesToScreen(double x, double y, double z){
        int screenCenterX = windowWidth/2 - (int)readerX;
        int screenCenterY = windowHeight/2 - (int)readerY;

        int screenX = screenCenterX + (int)(scale*x);
        int screenY = screenCenterY + (int)(scale*y);
        int[] coords = {screenX,screenY};
        scaleBar = 25000/scale;

        return coords;

    }


    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        if(e.getKeyCode() == KeyEvent.VK_SPACE){
            paused = !paused;
        }
        if(e.getKeyCode() == KeyEvent.VK_ENTER){
            initializeReader();
        }

        int moveSpeed = 10;
        if(e.getKeyCode() == KeyEvent.VK_LEFT){
            readerX -= moveSpeed;
        }
        if(e.getKeyCode() == KeyEvent.VK_RIGHT){
            readerX += moveSpeed;
        }
        if(e.getKeyCode() == KeyEvent.VK_UP){
            readerY -= moveSpeed;
        }
        if(e.getKeyCode() == KeyEvent.VK_DOWN){
            readerY += moveSpeed;
        }
        if(e.getKeyCode() == KeyEvent.VK_C){
            show_columns = !show_columns;
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }

    @Override
    public void mouseWheelMoved(MouseWheelEvent e) {

//        scalePow -= (double)e.getUnitsToScroll()/60;
//        scale = Math.pow(10,scalePow);
//        if(scale > scaleMax){
//            scale = scaleMax;
//        }
//        if(scale < scaleMin){
//            scale = scaleMin;
//        }
//        System.out.println(scale);




    }
}