package com.example.uday_vig.heatmap;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

public class HomeActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {

    Spinner timeSpinner, diseaseSpinner;
    Button mButton;
    StringBuilder sb = new StringBuilder();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        timeSpinner = findViewById(R.id.timeSpinner);
        diseaseSpinner = findViewById(R.id.diseaseSpinner);
        mButton = findViewById(R.id.button);

        getSupportActionBar().setTitle("Epidemic Spread");

        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.time_array, R.layout.spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        timeSpinner.setAdapter(adapter);

        ArrayAdapter<CharSequence> adapter2 = ArrayAdapter.createFromResource(this,
                R.array.disease_array, R.layout.spinner_item2);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        diseaseSpinner.setAdapter(adapter2);

        mButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int temp = diseaseSpinner.getSelectedItemPosition() + 1;
                String str = timeSpinner.getSelectedItem().toString() + " " + temp;
                Intent intent = new Intent(HomeActivity.this, MapsActivity.class);
                intent.putExtra("STR", str);
                startActivity(intent);
            }
        });
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        Spinner s1, s2;
        s1 = (Spinner) parent;
        s2 = (Spinner) parent;

        if(s1.getId() == R.id.timeSpinner){
            sb.append(s1.getItemAtPosition(position).toString() + " ");
        }else if(s2.getId() == R.id.diseaseSpinner){
            sb.append(s2.getItemAtPosition(position).toString());
        }
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }

    @Override
    protected void onStop() {
        startService(new Intent(this, NotifService.class));
        super.onStop();
    }
}
