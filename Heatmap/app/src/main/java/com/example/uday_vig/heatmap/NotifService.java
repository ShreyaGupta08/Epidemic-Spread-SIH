package com.example.uday_vig.heatmap;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.NotificationManagerCompat;
import android.util.Log;

import java.util.Timer;
import java.util.TimerTask;

public class NotifService extends Service {
    Timer timer;
    TimerTask timerTask;
    String TAG = "Timers";
    int Your_X_SECS = 5;
    Context context = this;


    @Override
    public IBinder onBind(Intent arg0) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.e(TAG, "onStartCommand");
        super.onStartCommand(intent, flags, startId);

        startTimer();

        return START_STICKY;
    }


    @Override
    public void onCreate() {
        Log.e(TAG, "onCreate");


    }

    @Override
    public void onDestroy() {
        Log.e(TAG, "onDestroy");
        stoptimertask();
        super.onDestroy();


    }

    //we are going to use a handler to be able to run in our TimerTask
    final Handler handler = new Handler();


    public void startTimer() {
        //set a new Timer
        timer = new Timer();

        //initialize the TimerTask's job
        initializeTimerTask();

        //schedule the timer, after the first 5000ms the TimerTask will run every 10000ms
        timer.schedule(timerTask, 5000, Your_X_SECS * 1000); //
        //timer.schedule(timerTask, 5000,1000); //
    }

    public void stoptimertask() {
        //stop the timer, if it's not already null
        if (timer != null) {
            timer.cancel();
            timer = null;
        }
    }

    public void initializeTimerTask() {

        timerTask = new TimerTask() {
            public void run() {

                //use a handler to run a toast that shows the current timestamp
                handler.post(new Runnable() {
                    public void run() {

                        Log.e("YOLO", "run: Service runs");

                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=1");
                        /*new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=2");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=3");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=4");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=5");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=6");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=7");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=8");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=9");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=10");
                        new GetNotifData(context).execute("http://07b92f1b.ngrok.io/fetch_cases/?days=30&diseaseid=11");*/

                        /*if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            CharSequence name = context.getString(R.string.channel_name);
                            String description = context.getString(R.string.channel_description);
                            int importance = NotificationManager.IMPORTANCE_DEFAULT;
                            NotificationChannel channel = new NotificationChannel("1", name, importance);
                            channel.setDescription(description);
                            NotificationManager notificationManager = context.getSystemService(NotificationManager.class);
                            notificationManager.createNotificationChannel(channel);
                        }


                        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(context, "1")
                                .setSmallIcon(R.drawable.ic_launcher_background)
                                .setContentTitle("Title")
                                .setContentText("Content")
                                .setPriority(NotificationCompat.PRIORITY_DEFAULT);

                        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
                        notificationManager.notify(7, mBuilder.build());
*/

                    }
                });
            }
        };
    }
}
