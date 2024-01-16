/*
    Arduino and ADXL345 Accelerometer - 3D Visualization Example 
     by Dejan, https://howtomechatronics.com
*/

import java.awt.event.KeyEvent;
import java.io.IOException;
import redis.clients.jedis.Jedis;

String data="";
float roll, pitch;

   Jedis jedis = new Jedis("192.168.43.165", 6379);

void setup() {
  size (960, 640, P3D);
    
  System.out.println("Connected to Redis");

}

void draw() {
  translate(width/2, height/2, 0);
  background(33);
  textSize(22);
  
  float x = Float.parseFloat(jedis.get("x"));
  float y = Float.parseFloat(jedis.get("y"));
  float z = Float.parseFloat(jedis.get("z"));
  
  System.out.println(x);
  System.out.println(y);
  System.out.println(z);
  System.out.println("");
  

  float roll = Float.parseFloat(jedis.get("roll"));
  float pitch = Float.parseFloat(jedis.get("pitch"));
  
  text("Roll: " + int(roll) + "     Pitch: " + int(pitch), -100, 265);

  // Rotate the object
  rotateX(radians(roll));
  rotateZ(radians(-pitch));
  
  // 3D 0bject
  textSize(30);  
  fill(0, 76, 153);
  box (386, 40, 200); // Draw box
  textSize(25);
  fill(255, 255, 255);
  text("      Tehnički fakultet u Rijeci", -183, 10, 101);

  //delay(10);
  //println("ypr:\t" + angleX + "\t" + angleY); // Print the values to check whether we are getting proper values
}
