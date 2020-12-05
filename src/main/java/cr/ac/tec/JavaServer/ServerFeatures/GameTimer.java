package cr.ac.tec.JavaServer.ServerFeatures;

import java.util.Timer;
import java.util.TimerTask;

public class GameTimer {
    private Timer timer = new Timer();
    private int currentTime = 0;

    TimerTask task = new TimerTask() {
        public void run() {
            currentTime++;
            System.out.println("Current seconds: " + currentTime);
            if (currentTime == 120){
                task.cancel();
                System.out.println("Stop timer");
            }

        }
    };

    public void start() {
        timer.scheduleAtFixedRate(task, 1000, 1000);
    }

    public static void main(String[] args) {
        GameTimer myTimer = new GameTimer();
        myTimer.start();
    }

    public int getcurrentTime() {
        return currentTime;
    }

}
