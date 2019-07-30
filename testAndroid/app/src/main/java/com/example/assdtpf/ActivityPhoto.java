package com.example.assdtpf;

/** https://examples.javacodegeeks.com/android/core/graphics/canvas-graphics/android-canvas-example/
 *
 */

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

public class ActivityPhoto extends AppCompatActivity {
    Button buttonLoadPicture;
    Button clearButton;
    Button processButton;

    Bitmap selectedBitmap;
    ImageProcessor processor;

    ImageView imgView;
    final Integer RESULT_LOAD_IMAGE = 1;
    com.javacodegeeks.androidcanvasexample.CanvasView customCanvas;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_photo);

        buttonLoadPicture = findViewById(R.id.buttonLoadPicture);
        clearButton = findViewById(R.id.buttonClear);
        processButton = findViewById(R.id.ProcessButton);

        customCanvas = (com.javacodegeeks.androidcanvasexample.CanvasView) findViewById(R.id.Canvas);

        buttonLoadPicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(
                        Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                startActivityForResult(i, RESULT_LOAD_IMAGE);
            }
        });

        clearButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                customCanvas.clearCanvas();
            }
        });

        processButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                process();
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK && null != data) {
            Uri selectedImage = data.getData();
            String[] filePathColumn = {MediaStore.Images.Media.DATA};

            Cursor cursor = getContentResolver().query(selectedImage,
                    filePathColumn, null, null, null);
            cursor.moveToFirst();

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            String picturePath = cursor.getString(columnIndex);
            cursor.close();

            Log.d("ImageEditLogs","Loading image from " + picturePath);

            // String picturePath contains the path of selected Image
            Bitmap image = BitmapFactory.decodeFile(picturePath);
            //imgView.setImageBitmap(image);
            selectedBitmap = image;

            customCanvas.setmBitmap(image);

        }
    }
    public void clearCanvas(View v) {
        customCanvas.clearCanvas();
    }

    public void process(){
        processor.setBitmap(selectedBitmap);
        processor.setPath(customCanvas.getPath());

        processor.computeContours();
    }
}
