/**
author: Sisi Duan. 
Implemented a simple key store interface so that we can deal with the storage and encryption in the python module 
 */
package bftsmart.demo.keyvalue;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutput;
import java.io.DataOutputStream;
import java.io.IOException;

import java.util.Arrays;
import java.security.SecureRandom;
import java.security.PrivateKey;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import bftsmart.tom.ServiceProxy;
import bftsmart.tom.util.Logger;
import bftsmart.tom.AsynchServiceProxy;
import bftsmart.tom.RequestContext;
import bftsmart.tom.core.messages.TOMMessage;
import bftsmart.tom.core.messages.TOMMessageType;
import bftsmart.tom.util.TOMUtil;

/**
 * Example client that updates a BFT replicated service (a Key-Value Store).
 * 
 * @author sisi
 */
public class KVClient {

    private static ClientThread[] recvPool = null;
    private static ExecutorService executor = null;
    private static int initID;
    private static int nextID;

    //private static AsynchServiceProxy KVProxy;
    private static ReplyListener KVProxy;


    public static void test(){
        System.out.println("test jpype\n");
    }

    public static void passArg(String[] args) throws IOException{
    //public static void main(String[] args) throws IOException{
        if (args.length < 2) {
            System.out.println("Usage: java ... KVClient <process id> <increment> [<pool size>]");
            System.out.println("       if <increment> equals 0 the request will be read-only");
            System.out.println("       default <pool size> equals 1");
            System.exit(-1);
        }

        //ServiceProxy KVProxy = new ServiceProxy(Integer.parseInt(args[0]));
        initID = Integer.parseInt(args[0]);
        nextID = initID + 1;
        //KVProxy = new AsynchServiceProxy(initID,"./config/");
        KVProxy = new ReplyListener(initID);

        //System.out.println("-------initID "+ initID+"\n");
        Logger.debug = false;

        int inc = Integer.parseInt(args[1]);
        int pool = (args.length > 2) ? Integer.parseInt(args[2]) : 1; //Integer.parseInt(args[2]);
        //System.out.println(pool)
        
    }

    public static void sendRequest(String input) throws IOException{
        try {

            System.out.println("Start processing requests..."+input+"\n");
            /*executor = Executors.newFixedThreadPool(pool);

            for (int i = 0; i< pool; i++){
                System.out.println("Start ClientThread...");
                executor.execute(new ClientThread(initID));
                //nextID++;
            }*/

            for (int i=0;i<1;i++){
                byte[] tmp = input.getBytes();

                //byte[] tmp = new byte[]{};
                System.out.println("invoking request "+i+", payload: "+tmp+"\n");
                KVProxy.invokeAsynchRequest(assembleRequest("SEQUENCE",Integer.toString(initID),tmp),null,TOMMessageType.ORDERED_REQUEST);
            }

        } catch(IOException | NumberFormatException e){
            e.printStackTrace();
        }

    }

    public static void main(String[] args) throws IOException{
        if (args.length < 2) {
            System.out.println("Usage: java ... KVClient <process id> <increment> [<pool size>]");
            System.out.println("       if <increment> equals 0 the request will be read-only");
            System.out.println("       default <pool size> equals 1");
            System.exit(-1);
        }

        initID = Integer.parseInt(args[0]);
        nextID = initID + 1;
        //KVProxy = new AsynchServiceProxy(initID,"./config/");
        KVProxy = new ReplyListener(initID);

        //System.out.println("-------initID "+ initID+"\n");
        Logger.debug = false;

        int inc = Integer.parseInt(args[1]);
        int pool = (args.length > 2) ? Integer.parseInt(args[2]) : 1; //Integer.parseInt(args[2]);

        try {

            System.out.println("Start processing requests...");

            for (int i=0;i<5;i++){
                byte[] tmp = "TEST".getBytes();

                //byte[] tmp = new byte[]{};
                System.out.println("invoking request "+i+", payload: "+tmp+"\n");
                KVProxy.invokeAsynchRequest(assembleRequest("SEQUENCE",Integer.toString(initID),tmp),null,TOMMessageType.ORDERED_REQUEST);
            }

        } catch(IOException | NumberFormatException e){
            e.printStackTrace();
        }
        
    }

    public static byte[] assembleRequest(String type, String channelID, byte[] payload) throws IOException {
            
        PrivateKey key = KVProxy.getViewManager().getStaticConf().getRSAPrivateKey();        
            
        ByteArrayOutputStream bos = new ByteArrayOutputStream(type.length() + channelID.length() + payload.length);
        DataOutput out = new DataOutputStream(bos);


        out.writeUTF(type);
        out.writeUTF(channelID);
        out.writeInt(payload.length);
        out.write(payload);

        
        bos.flush();
        bos.close();

        //System.out.println("assemble "+type + " type\n");
        //System.out.println("assemble channel ID: "+channelID + "\n");

        byte[] msg = bos.toByteArray();
        
        byte[] sig = TOMUtil.signMessage(key, msg);
        
        bos = new ByteArrayOutputStream(msg.length+sig.length);
        out = new DataOutputStream(bos);
        
        out.writeInt(msg.length);
        out.write(msg);
        out.writeInt(sig.length);
        out.write(sig);

        //System.out.println("sig: "+sig +"\n");
        
        bos.flush();
        bos.close();
        
        return bos.toByteArray();
    }

    private static class ClientThread extends Thread {
            private int id;
            private DataInputStream input;
            private AsynchServiceProxy out;

            public ClientThread(int id) throws IOException{
                //Sisi: For now we just use random bytes. Later it needs to be extended to receive bytes either directly from 
                //Python script or through a thread/buffer
                this.id = id;
                this.out = new AsynchServiceProxy(this.id, "./config/");
            }

            private static String readString(DataInputStream is) throws IOException {
                
                byte[] bytes = readBytes(is);
                
                return new String(bytes);
                
            }

            private static long readLong(DataInputStream is) throws IOException {
                byte[] buffer = new byte[8];

                is.read(buffer);

                //This is for little endian
                //long value = 0;
                //for (int i = 0; i < by.length; i++)
                //{
                //   value += ((long) by[i] & 0xffL) << (8 * i);
                //}
                //This is for big endian
                long value = 0;
                for (int i = 0; i < buffer.length; i++) {
                    value = (value << 8) + (buffer[i] & 0xff);
                }

                return value;
            }

            private static byte[] readBytes(DataInputStream is) throws IOException {
                
                System.out.println("readbytes\n");
                long size = readLong(is);

                //logger.debug("Read number of bytes: " + size);
                System.out.println("Read number of bytes: " + size+"\n");

                byte[] bytes = new byte[(int) size];

                is.read(bytes);
                System.out.println("Read all bytes!\n" );
                //logger.debug("Read all bytes!");

                return bytes;

            }

            private static byte[] serializeRequest(String type, String channelID, byte[] payload) throws IOException {
                    
                ByteArrayOutputStream bos = new ByteArrayOutputStream(type.length() + channelID.length() + payload.length);
                DataOutput out = new DataOutputStream(bos);

                out.writeUTF(type);
                out.writeUTF(channelID);
                out.writeInt(payload.length);
                out.write(payload);

                bos.flush();

                bos.close();
                
                return bos.toByteArray();
            }

            public void run() {
                String id;
                SecureRandom random = new SecureRandom();
                byte[] env= new byte[7];
                random.nextBytes(env);

                //while(true){
                    try{
                        //id = readString(this.input);
                        //env = readBytes(this.input);
                        id = "0";

                        System.out.println("before invoking...\n");
                        this.out.invokeAsynchRequest(serializeRequest("CONFIG",id,env), new bftsmart.communication.client.ReplyListener(){
                        

                            private int replies = 0;
                            @Override
                            public void reset(){
                                replies = 0;
                            }

                            @Override
                                public void replyReceived(RequestContext rc, TOMMessage tomm) {
                                    //System.out.println(tomm.)
                                    if (Arrays.equals(tomm.getContent(), "ACK".getBytes())){
                                         replies++;
                                    }

                                    double q = Math.ceil((double) (out.getViewManager().getCurrentViewN() + out.getViewManager().getCurrentViewF() + 1) / 2.0);

                                    if (replies >= q) {
                                        out.cleanAsynchRequest(rc.getOperationId());
                                    }
                                    //System.out.println("getting reply "+replies+"\n");
                                }
                        }, TOMMessageType.ORDERED_REQUEST);
                        System.out.println("config done...\n");

                    }catch (IOException ex) {
                            //Logger.getLogger(BFTProxy.class.getName()).log(Level.SEVERE, null, ex);
                            //continue;
                        }
                //}
        }

}

}

