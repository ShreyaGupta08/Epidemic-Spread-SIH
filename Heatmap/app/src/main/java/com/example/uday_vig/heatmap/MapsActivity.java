package com.example.uday_vig.heatmap;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Tile;
import com.google.android.gms.maps.model.TileOverlay;
import com.google.android.gms.maps.model.TileOverlayOptions;
import com.google.maps.android.heatmaps.HeatmapTileProvider;

import java.util.ArrayList;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private static final int LOCATION_REQUEST = 1;
    public String days;
    public String[] res = new String[4];
    public Button refresh, hospitalFinder;
    public Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        context = this;

        Intent intent = getIntent();
        String req = intent.getStringExtra("STR");

        refresh = findViewById(R.id.refresh);
        hospitalFinder = findViewById(R.id.hospitalFinder);

        /*refresh.setBackgroundColor(Color.parseColor("#25D366"));
        hospitalFinder.setBackgroundColor(Color.parseColor("#25D366"));*/

        Log.e("YOLO", "onCreate: " + req);

        res = req.split(" ");

        days = res[1];

        Log.e("Days", "onCreate: " + days + " " + res[3]);

        if(ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(MapsActivity.this, new String[] {Manifest.permission.ACCESS_FINE_LOCATION},
                    LOCATION_REQUEST);
        }
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        /*// Add a marker in Sydney and move the camera
        LatLng sydney = new LatLng(22.303301, 74.3591);
        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Alirajpur"));*/

        refresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new GetData(context).execute(mMap, "https://07b92f1b.ngrok.io/fetch_cases/?days=" + days + "&diseaseid=" + res[3]);
            }
        });

        hospitalFinder.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent launchIntent = getPackageManager().getLaunchIntentForPackage("com.example.uday_vig.mapsparticularnearbyplace");
                if (launchIntent != null) {
                    startActivity(launchIntent);//null pointer check in case package name was not found
                }
            }
        });

        new GetData(context).execute(mMap, "https://07b92f1b.ngrok.io/fetch_cases/?days=" + days + "&diseaseid=" + res[3]);

        /*ArrayList<LatLng> list = new ArrayList<>()

        list.add(new LatLng(22.303301, 74.3591));
        list.add(new LatLng(21.97794, 76.622932));
        list.add(new LatLng(21.87886, 75.74766));
        list.add(new LatLng(24.076836, 75.069298));
        list.add(new LatLng(24.476385, 74.862411));*/

        /*HeatmapTileProvider mProvider;
        TileOverlay mOverlay;

        mProvider = new HeatmapTileProvider.Builder()
                .data(list)
                .build();
        // Add a tile overlay to the map, using the heat map tile provider.
        mOverlay = mMap.addTileOverlay(new TileOverlayOptions().tileProvider(mProvider));*/
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if(grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED){
            switch (requestCode){
                case LOCATION_REQUEST:
                    Toast.makeText(this, "Granted", Toast.LENGTH_SHORT).show();
            }
        }
    }
}

//epidemic.pythonanywhere.com/similar_states/?state=Ujjain
