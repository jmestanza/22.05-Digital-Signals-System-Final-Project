package com.javacodegeeks.androidcanvasexample;

import android.content.Context;
import android.graphics.*;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;

public class CanvasView extends View {

    public int width;
    public int height;
    private Bitmap mBitmap;
    private Canvas mCanvas;
    private Path mPath;
    Context context;
    private Paint mPaint, mPaint2;
    private float mX, mY;
    private static final float TOLERANCE = 5;
    private Bitmap backgroundBitmap;
    private int w,h;
    private Bitmap maskBitmap;
    private boolean enabled;

    public CanvasView(Context c, AttributeSet attrs) {
        super(c, attrs);
        context = c;

        // we set a new Path
        mPath = new Path();

        // and we set a new Paint with the desired attributes
        mPaint = new Paint();
        mPaint.setAntiAlias(true);
        mPaint.setColor(Color.BLACK);
        mPaint.setStyle(Paint.Style.STROKE);
        mPaint.setStrokeJoin(Paint.Join.ROUND);
        mPaint.setStrokeWidth(4f);
        //mBitmap = Bitmap.createBitmap(100, 200, Bitmap.Config.ARGB_8888);
        maskBitmap = null;

        mPaint2 = new Paint();
        mPaint2.setAntiAlias(true);
        mPaint2.setColor(Color.BLACK);
        mPaint2.setStyle(Paint.Style.STROKE);
        mPaint2.setStrokeJoin(Paint.Join.ROUND);
        mPaint2.setStrokeWidth(4f);
        mPaint2.setAlpha(50);

        enabled = true;
    }

    // override onSizeChanged
    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);

        // your Canvas will draw onto the defined Bitmap

        backgroundBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
        mBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
        mCanvas = new Canvas(mBitmap);

        this.w = w;
        this.h = h;
    }


    // override onDraw
    @Override
    protected void onDraw(Canvas canvas) {

        super.onDraw(canvas);

        canvas.drawBitmap(backgroundBitmap,
                new Rect(0,0,backgroundBitmap.getWidth(),backgroundBitmap.getHeight()),
                new Rect(0,0,mBitmap.getWidth(),mBitmap.getHeight()),
                mPaint
        );
        if (maskBitmap != null){

            canvas.drawBitmap(maskBitmap,
                    new Rect(0,0,backgroundBitmap.getWidth(),backgroundBitmap.getHeight()),
                    new Rect(0,0,mBitmap.getWidth(),mBitmap.getHeight()),
                    mPaint2
            );
        }
        // draw the mPath with the mPaint on the canvas when onDraw
        canvas.drawPath(mPath, mPaint);
    }

    // when ACTION_DOWN start touch according to the x,y values
    private void startTouch(float x, float y) {
        mPath.moveTo(x, y);
        mX = x;
        mY = y;
    }

    // when ACTION_MOVE move touch according to the x,y values
    private void moveTouch(float x, float y) {
        float dx = Math.abs(x - mX);
        float dy = Math.abs(y - mY);
        if (dx >= TOLERANCE || dy >= TOLERANCE) {
            mPath.quadTo(mX, mY, (x + mX) / 2, (y + mY) / 2);
            mX = x;
            mY = y;
        }
    }

    public void clearCanvas() {
        mPath.reset();
        invalidate();

    }

    // when ACTION_UP stop touch
    private void upTouch() {
        mPath.lineTo(mX, mY);
    }

    //override the onTouchEvent
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (enabled) {
            float x = event.getX();
            float y = event.getY();

            switch (event.getAction()) {
                case MotionEvent.ACTION_DOWN:
                    startTouch(x, y);
                    invalidate();
                    break;
                case MotionEvent.ACTION_MOVE:
                    moveTouch(x, y);
                    invalidate();
                    break;
                case MotionEvent.ACTION_UP:
                    upTouch();
                    invalidate();
                    break;
            }
        }
        return true;
    }

    public Bitmap getmBitmap() {
        return mBitmap;
    }

    public void setmBitmap(Bitmap bitmap) {

        //Bitmap mutableBitmap = mBitmap.copy(Bitmap.Config.ARGB_8888, true);

        //Paint paint = new Paint();
        //paint.setAntiAlias(true);
       // paint.setFilterBitmap(true);
        //paint.setDither(true);
        //this.mCanvas.drawColor(0xFFAAAAAA);

        this.backgroundBitmap = bitmap;

    }
    public Path getPath(){
        return mPath;
    }
    public Bitmap getCanvasBitmap(){
        Bitmap bitmap = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);

        Canvas canvas = new Canvas(bitmap);
        canvas.drawRGB(255,255,255);
        canvas.drawPath(mPath, mPaint);


        return bitmap;
    }
    public void setMaskBitmap(Bitmap bitmap){
        this.maskBitmap = bitmap;
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }

    @Override
    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}