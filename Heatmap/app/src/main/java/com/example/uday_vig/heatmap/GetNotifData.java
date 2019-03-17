package com.example.uday_vig.heatmap;

import android.Manifest;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.AsyncTask;
import android.os.Build;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.NotificationManagerCompat;
import android.util.Log;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.tasks.OnSuccessListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.Charset;
import java.text.DecimalFormat;
import java.util.ArrayList;

public class GetNotifData extends AsyncTask<String, Void, String> {

    private FusedLocationProviderClient mFusedLocationProviderClient;
    private Location mLocation;
    private Context context;
    public String urlStr;

    public GetNotifData(Context context) {
        this.context = context;
    }

    @Override
    protected String doInBackground(String... strings) {
        urlStr = strings[0];
        String jsonResponse = "";
        HttpURLConnection urlConnection = null;
        InputStream inputStream = null;
        try {
            URL url = new URL(urlStr);
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setReadTimeout(10000);
            urlConnection.setConnectTimeout(15000);

            urlConnection.setRequestMethod("GET");
            urlConnection.connect();

            if (urlConnection.getResponseCode() == 200) {
                inputStream = urlConnection.getInputStream();
                jsonResponse = readFromStream(inputStream);
            } else {
                Log.e("FAST", "Error response code: " + urlConnection.getResponseCode());
            }
        } catch (IOException e) {
            Log.e("FAST", "Problem retrieving the JSON results.", e);
        } finally {
            if (urlConnection != null) {
                urlConnection.disconnect();
            }
            if (inputStream != null) {
                try {
                    inputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return jsonResponse;
    }

    @Override
    protected void onPostExecute(String s) {

        Log.e("YOLO", "onPostExecute: " + s);

        mFusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(context);

        if(ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) ==
                PackageManager.PERMISSION_GRANTED){
            mFusedLocationProviderClient.getLastLocation().addOnSuccessListener(new OnSuccessListener<Location>() {
                @Override
                public void onSuccess(Location location) {
                    mLocation = location;
                }
            });
        }


        ArrayList<LatLng> list = new ArrayList<>();

        try {
            JSONObject root = new JSONObject(s);
            JSONArray predictedDist = root.getJSONArray("predicted_districts");
            list.add(new LatLng(9.211351, 76.640198));
            if(predictedDist.length() != 10000){
                for(int i = 0; i < predictedDist.length(); i++){
                    String[] temporary = predictedDist.get(i).toString().split(" ");
                    list.add(new LatLng(Double.parseDouble(temporary[1]), Double.parseDouble(temporary[0])));
                }



                for(int i = 0; i < list.size(); i++){
                    if(dist(new LatLng(mLocation.getLatitude(), mLocation.getLongitude()), list.get(i)) < 30000){
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                            CharSequence name = context.getString(R.string.channel_name);
                            String description = context.getString(R.string.channel_description);
                            int importance = NotificationManager.IMPORTANCE_DEFAULT;
                            NotificationChannel channel = new NotificationChannel("1", name, importance);
                            channel.setDescription(description);
                            NotificationManager notificationManager = context.getSystemService(NotificationManager.class);
                            notificationManager.createNotificationChannel(channel);
                        }

                        char ch = urlStr.charAt(urlStr.length() - 1);
                        char pch = urlStr.charAt(urlStr.length() - 2);
                        String title = "Epidemic X";

                        if(ch == '1' && pch != '1'){
                            title = "AIDS";
                        }else if(ch == '2'){
                            title = "Malaria";
                        }else if(ch == '3'){
                            title = "Cholera";
                        }else if(ch == '4'){
                            title = "Smallpox";
                        }else if(ch == '5'){
                            title = "Tuberculosis";
                        }else if(ch == '6'){
                            title = "Influenza";
                        }else if(ch == '7'){
                            title = "Dengue";
                        }else if(ch == '8'){
                            title = "Chikungunya";
                        }else if(ch == '9'){
                            title = "Ebola";
                        }else if(ch == '0' && pch == '1'){
                            title = "Meningitis";
                        }

                        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(context, "1")
                                .setSmallIcon(R.drawable.ic_launcher_background)
                                .setContentTitle("ALERT! Outbreak of " + title)
                                .setContentText("Click Here To Know More.")
                                .setPriority(NotificationCompat.PRIORITY_DEFAULT);

                        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
                        notificationManager.notify(7, mBuilder.build());

                        break;
                    }
                }
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private static String readFromStream(InputStream inputStream) throws IOException {
        StringBuilder output = new StringBuilder();
        if (inputStream != null) {
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream, Charset.forName("UTF-8"));
            BufferedReader reader = new BufferedReader(inputStreamReader);
            String line = reader.readLine();
            while (line != null) {
                output.append(line);
                line = reader.readLine();
            }
        }
        return output.toString();
    }

    public double dist(LatLng StartP, LatLng EndP) {
        int Radius = 6371;// radius of earth in Km
        double lat1 = StartP.latitude;
        double lat2 = EndP.latitude;
        double lon1 = StartP.longitude;
        double lon2 = EndP.longitude;
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);
        double a = Math.sin(dLat / 2) * Math.sin(dLat / 2)
                + Math.cos(Math.toRadians(lat1))
                * Math.cos(Math.toRadians(lat2)) * Math.sin(dLon / 2)
                * Math.sin(dLon / 2);
        double c = 2 * Math.asin(Math.sqrt(a));
        double valueResult = Radius * c;
        double km = valueResult / 1;
        DecimalFormat newFormat = new DecimalFormat("####");
        int kmInDec = Integer.valueOf(newFormat.format(km));
        double meter = valueResult % 1000;
        int meterInDec = Integer.valueOf(newFormat.format(meter));
        Log.i("Radius Value", "" + valueResult + "   KM  " + kmInDec
                + " Meter   " + meterInDec);

        return Radius * c;
    }
}
