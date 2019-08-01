package com.example.assdtpf;

/** https://examples.javacodegeeks.com/android/core/graphics/canvas-graphics/android-canvas-example/
 *
 */

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
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
    private String status;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_photo);


        processor = new ImageProcessor(ActivityPhoto.this);

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
                customCanvas.setMaskBitmap(null);
                customCanvas.clearCanvas();
                status = "Select border";
                processButton.setText(R.string.Select);
                customCanvas.setEnabled(true);
            }
        });

        processButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (status.equals("Select border")) {
                    process();
                }else if (status.equals("Wait for confirm")){
                    startAlgorithm();
                }
            }
        });
        status = "Select border";
        customCanvas.setEnabled(true);
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


            // Rotamos 90 grados
            Matrix matrix = new Matrix();
            matrix.postRotate(90);
            Bitmap rotatedBitmap = Bitmap.createBitmap(image, 0, 0, image.getWidth(), image.getHeight(), matrix, true);


            selectedBitmap = rotatedBitmap;

            customCanvas.setmBitmap(selectedBitmap.copy(selectedBitmap.getConfig(), false));

        }
    }
    public void clearCanvas(View v) {
        customCanvas.clearCanvas();
    }

    public void process(){
        processor.setBitmap(selectedBitmap.copy(selectedBitmap.getConfig(), false));
        processor.setPath(customCanvas.getCanvasBitmap());

        processor.computeContours();

        customCanvas.clearCanvas();

        customCanvas.setMaskBitmap(processor.getFloodedBitmap());
        status = "Wait for confirm";
        customCanvas.setEnabled(false);

        processButton.setText(R.string.Process);

    }

    public void startAlgorithm(){
        // empezamos el algoritmo
        // vamos a editar la imagen

        processor.runIteration();

    }
}
