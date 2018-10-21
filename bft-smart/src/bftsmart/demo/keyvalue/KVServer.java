
/**
author: Sisi Duan. 
Implemented a simple key store interface so that we can deal with the storage and encryption in the python module 
 */

package bftsmart.demo.keyvalue;

import bftsmart.tom.MessageContext;
import bftsmart.tom.ServiceReplica;
//import bftsmart.tom.server.defaultservices.DefaultSingleRecoverable;
import bftsmart.tom.server.defaultservices.DefaultRecoverable;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInput;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.io.IOException;
import java.io.ByteArrayInputStream;
import java.net.ServerSocket;
import java.net.Socket;

import java.nio.ByteBuffer;

public final class KVServer extends DefaultRecoverable  {
    public final static String DEFAULT_CONFIG_FOLDER = "./config/";
    private int id;
    private ServiceReplica replia = null;
    private String configFolder;
    private int sequence = 0;
    private static DataOutputStream fos;

    private static ServerSocket forwardServer = null;
    private static Socket forwardSocket = null;

    public KVServer(int id){ //throws IOException {
        this.id = id;
        //this.configFolder = (configFolder != null ? configFolder: KVServer.DEFAULT_CONFIG_FOLDER);
        this.sequence = 0;
    	new ServiceReplica(this.id, this, this);
    }

    public static void test(){
        System.out.println("test jpype server\n");
    }

    public static void passArgs(String[] args){
    //public static void main(String[] args){
        if(args.length < 1) {
            System.out.println("Use: java KVServer <processId>");
            System.exit(-1);
        }      
        
        int myID=Integer.parseInt(args[0]);
        new KVServer(myID);
        
    }

    public static void main(String[] args){
        if(args.length < 1) {
            System.out.println("Use: java KVServer <processId>");
            System.exit(-1);
        }      

        int myID=Integer.parseInt(args[0]);
        new KVServer(myID);
        
    }

    
            
    @Override
    public byte[] appExecuteUnordered(byte[] command, MessageContext msgCtx) {   
        System.out.println("unordered\n");      
        //TODO: Need to figure out for read requests
        return new byte[0];
    }

    @Override
    public byte[][] appExecuteBatch(byte[][] commands, MessageContext[] msgCtxs, boolean fromConsensus) {   

        byte[][] replies = new byte[commands.length][];
        for (int i = 0; i<commands.length; i++){
            if(msgCtxs!=null && msgCtxs[i]!=null){
                try{
                    replies[i] = executeSingle(commands[i],msgCtxs[i],fromConsensus);
                }catch(IOException ex){
                    ex.printStackTrace();
                }
            }
        }
        return replies;    
    } 
  
    private byte[] executeSingle(byte[] command, MessageContext msgCtx, boolean fromConsensus) throws IOException{
        //System.out.println("Execute single\n");
        RequestTuple tuple = deserializeSignedRequest(command);
        if (tuple.type.equals("CONFIG")){
            System.out.println("---Config request\n");
        }//We do not have config messages for now. It might be useful in the future

        if (tuple.type.equals("SEQUENCE")){
            System.out.println("---Sequence\n");
            byte[][] reply = new byte[2][];
            //System.out.println("channelID: "+tuple.channelID+"\n");
            //System.out.println("payload: "+tuple.payload+"\n");
            //System.out.println("payload: "+new String(tuple.payload)+"\n");
            reply[0] = "SEQUENCE".getBytes();
            reply[1] = ByteBuffer.allocate(4).putInt(this.sequence).array();
            //reply[2] = tuple.payload;
            
            //TODO: Nedd to handle configuration file to avoid hard-coded host name and port number
            //We need to deliver sequence number -- this.sequence, client id -- channelID, and message content --payload
            int port = 5000+this.id;
            Socket socket = new Socket("localhost",port);
            byte[][] deliver = new byte[3][];
            deliver[0] = ByteBuffer.allocate(4).putInt(this.sequence).array();
            deliver[1] = ByteBuffer.allocate(4).putInt(Integer.parseInt(tuple.channelID)).array();
            deliver[2] = tuple.payload;
            //byte[] bytes = serializeContents(deliver);
            byte[] bytes = serializeDelivery(this.sequence,Integer.parseInt(tuple.channelID),tuple.payload);
            DataOutputStream fos = new DataOutputStream(socket.getOutputStream());
            //fos.writeInt(bytes.length);
            fos.write(bytes);
            /*fos.writeInt(this.sequence);
            fos.flush();
            fos.writeInt(Integer.parseInt(tuple.channelID));
            fos.flush();
            fos.writeUTF(new String(tuple.payload));*/
            fos.flush();
            fos.close();
            socket.close();

            this.sequence++;

            
            return serializeContents(reply);
        }

        return "ACK".getBytes();
    }

    private byte[] serializeDelivery(int sequence,int cid,byte[] msg) throws IOException {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        DataOutputStream out = new DataOutputStream(bos);

        out.writeInt(sequence);
        out.flush();
        bos.flush();

        out.writeInt(cid);
        out.flush();
        bos.flush();

        out.writeInt(msg.length);
        out.flush();
        bos.flush();

        out.write(msg);
        out.flush();
        bos.flush();

        out.close();
        bos.close();
        return bos.toByteArray();
    }

    private byte[] serializeContents(byte[][] contents) throws IOException {

        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        DataOutputStream out = new DataOutputStream(bos);

        out.writeInt(contents.length);

        out.flush();
        bos.flush();
        for (int i = 0; i < contents.length; i++) {

            out.writeInt(contents[i].length);

            out.write(contents[i]);

            out.flush();
            bos.flush();
        }

        out.close();
        bos.close();
        return bos.toByteArray();

    }

    private RequestTuple deserializeSignedRequest(byte[] request) throws IOException {
        
        ByteArrayInputStream bis = new ByteArrayInputStream(request);
        DataInput in = new DataInputStream(bis);
        
        int l = in.readInt();
        byte[] msg = new byte[l];
        in.readFully(msg);
        l = in.readInt();
        byte[] sig = new byte[l];
        in.readFully(sig);
        
        bis.close();
        
        bis = new ByteArrayInputStream(msg);
        in = new DataInputStream(bis);
        
        String type = in.readUTF();
        String channelID = in.readUTF();
        l = in.readInt();
        byte[] payload = new byte[l];
        in.readFully(payload);
      
        bis.close();

        /*System.out.println("---type, "+type+"\n");
        System.out.println("---channelID, "+channelID+"\n");
        System.out.println("---payload, "+payload+"\n");*/
        
        return new RequestTuple(type, channelID, payload, sig);
        
    }
    
    private RequestTuple deserializeRequest(byte[] request) throws IOException {
        
        ByteArrayInputStream bis = new ByteArrayInputStream(request);
        DataInput in = new DataInputStream(bis);
        
        String type = in.readUTF();
        String channelID = in.readUTF();
        int l = in.readInt();
        byte[] payload = new byte[l];
        in.readFully(payload);
      
        bis.close();
        

        return new RequestTuple(type, channelID, payload, null);
        
    }

    private RequestTuple deserializeSginedRequest(byte[] request) throws IOException {
        ByteArrayInputStream bis = new ByteArrayInputStream(request);
        DataInput in = new DataInputStream(bis);
        
        int l = in.readInt();
        byte[] msg = new byte[l];
        in.readFully(msg);
        l = in.readInt();
        byte[] sig = new byte[l];
        in.readFully(sig);
        
        bis.close();
        
        bis = new ByteArrayInputStream(msg);
        in = new DataInputStream(bis);
        
        String type = in.readUTF();
        String channelID = in.readUTF();
        l = in.readInt();
        byte[] payload = new byte[l];
        in.readFully(payload);
      
        bis.close();
        
        return new RequestTuple(type, channelID, payload, sig);
    }
    
    @SuppressWarnings("unchecked")
    @Override
    public void installSnapshot(byte[] state) {
        System.out.println("install snapshot...\n");
    //TODO: Need to be extended for a fully functional version
    }

    @Override
    public byte[] getSnapshot() {
        System.out.println("get snapshot...\n");
    //TODO: Need to be extended for a fully functional version
        return new byte[0];
    }
    
    

    private class RequestTuple{
        String type = null;
        String channelID = null;
        byte[] payload = null;
        byte[] signature = null;
        
        RequestTuple(String type, String channelID, byte[] payload, byte[] signature){
            this.type = type;
            this.channelID = channelID;
            this.payload = payload;
            this.signature = signature;
        }
    }
}
