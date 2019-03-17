package com.example.uday_vig.heatmap;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.support.v4.content.ContextCompat;
import android.util.Log;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.BitmapDescriptor;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.Circle;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.TileOverlay;
import com.google.android.gms.maps.model.TileOverlayOptions;
import com.google.maps.android.heatmaps.HeatmapTileProvider;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ContentHandler;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.Charset;
import java.util.ArrayList;

public class GetData extends AsyncTask<Object, Void, String> {

    GoogleMap map;
    Context context;

    public GetData(Context context) {
        this.context = context;
    }

    @Override
    protected String doInBackground(Object... strings) {
        map = (GoogleMap) strings[0];
        String timespan = (String) strings[1];
        Log.e("URL", "doInBackground: " + timespan);
        String jsonResponse = "";
        HttpURLConnection urlConnection = null;
        InputStream inputStream = null;
        try {
            URL url = new URL(timespan);
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setReadTimeout(10000);
            urlConnection.setConnectTimeout(15000);

            urlConnection.setRequestMethod("GET");
            urlConnection.connect();

            if (urlConnection.getResponseCode() == 200) {
                inputStream = urlConnection.getInputStream();
                jsonResponse = readFromStream(inputStream);
            } else {
                Log.e("Response", "Error response code: " + urlConnection.getResponseCode());
            }
        } catch (IOException e) {
            Log.e("Response", "Problem retrieving the JSON results.", e);
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
        HeatmapTileProvider mProvider;
        TileOverlay mOverlay;

        Log.e("Response", "onPostExecute: " + s);

        ArrayList<LatLng> list = new ArrayList<>();
        ArrayList<LatLng> pharmacyList = new ArrayList<>();
        ArrayList<LatLng> predictionsList = new ArrayList<>();
        ArrayList<String> predictionsColourList = new ArrayList<>();

        try {
            JSONObject root = new JSONObject(s);
            JSONArray arr = root.getJSONArray("cases");

            for(int i = 0; i < arr.length(); i++){
                JSONObject cases = (JSONObject) arr.get(i);

                String loc = cases.getString("location");
                String[] temp = loc.split(" ");

                list.add(new LatLng(Double.parseDouble(temp[0]), Double.parseDouble(temp[1])));
            }

            JSONObject pharmacies = root.getJSONObject("pharmacies");
            /*JSONObject temp = pharmacies.getJSONObject("1");
            String location = temp.getString("location");

            String[] tempStr = location.split(" ");

            pharmacyList.add(new LatLng(Double.parseDouble(tempStr[0]), Double.parseDouble(tempStr[1])));*/

            for(int i = 0; i < pharmacies.length(); i++){
                JSONObject temp = pharmacies.getJSONObject(i + 1 + "");

                String location = temp.getString("location");

                String[] tempStr = location.split(" ");

                pharmacyList.add(new LatLng(Double.parseDouble(tempStr[0]), Double.parseDouble(tempStr[1])));
            }

            JSONArray predictions = root.getJSONArray("predicted_districts");
            Log.e("TAG", "onPostExecute: "+predictions.length());
            for(int i = 0; i < predictions.length(); i++){
                String l = (String) predictions.get(i);
                String[] temp1 = l.split(" ");
                predictionsList.add(new LatLng(Double.parseDouble(temp1[1]), Double.parseDouble(temp1[0])));
                predictionsColourList.add(temp1[2]);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }


        if(!list.isEmpty()){
            mProvider = new HeatmapTileProvider.Builder()
                    .data(list)
                    .build();
            mOverlay = map.addTileOverlay(new TileOverlayOptions().tileProvider(mProvider));

            map.moveCamera(CameraUpdateFactory.newLatLng(list.get(0)));
        }

        for(int i = 0; i < pharmacyList.size(); i++){

            Drawable background = ContextCompat.getDrawable(context, R.drawable.ic_healing_black_24dp);
            background.setBounds(0, 0, background.getIntrinsicWidth(), background.getIntrinsicHeight());
            Drawable vectorDrawable = ContextCompat.getDrawable(context, R.drawable.ic_healing_black_24dp);
            vectorDrawable.setBounds(40, 20, vectorDrawable.getIntrinsicWidth() + 40, vectorDrawable.getIntrinsicHeight() + 20);
            Bitmap bitmap = Bitmap.createBitmap(background.getIntrinsicWidth(), background.getIntrinsicHeight(), Bitmap.Config.ARGB_8888);
            Canvas canvas = new Canvas(bitmap);
            background.draw(canvas);
            vectorDrawable.draw(canvas);
            BitmapDescriptor bitmapDescriptor = BitmapDescriptorFactory.fromBitmap(bitmap);

            map.addMarker(new MarkerOptions()
                    .position(pharmacyList.get(i))
                    .icon(bitmapDescriptor));
        }

        for(int i = 0; i < predictionsList.size(); i++){
            map.addMarker(new MarkerOptions().position(predictionsList.get(i)));
            Circle circle = map.addCircle(new CircleOptions()
                    .center(predictionsList.get(i))
                    .radius(30000)
                    .strokeColor(Color.BLACK)
                    .strokeWidth(0)
                    .fillColor(Color.parseColor(predictionsColourList.get(i))));
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
}