/*
author: Sisi Duan
Partially copied from bft-smart hyperledger git repo.
It is used at client side to deal with reply messages. 
TODO: Need to extend the script since I haven't touched too much for handling reply yet.
*/
package bftsmart.demo.keyvalue;

import bftsmart.reconfiguration.views.View;
import bftsmart.tom.AsynchServiceProxy;
import bftsmart.tom.core.messages.TOMMessage;
import bftsmart.tom.core.messages.TOMMessageType;
import bftsmart.tom.util.Extractor;
import bftsmart.tom.util.TOMUtil;
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

public class ReplyListener extends AsynchServiceProxy{

    private Map<Integer, ReplyTuple[]> replies;
    private Map<Integer, String> responses;
    private int replyQuorum;
    
    private int nextView;
    private View[] views;
    
    private int[] sequences;

    public ReplyListener(int id){
        super(id);
        init();
    }

    private void init(){
        responses = new ConcurrentHashMap<>();
        replies = new HashMap<>();
        replyQuorum = getReplyQuorum();

        nextView = getViewManager().getCurrentViewId();
        views = new View[getViewManager().getCurrentViewN()];
        
        sequences = new int[getViewManager().getCurrentViewN()];
        for (int i = 0; i < sequences.length; i++) {
            
            sequences[i] = -1;
        }
    }

    private int newSequence(byte[] bytes) {
        
        try {
            byte[][] contents = deserializeContents(bytes);
            //System.out.println("Sequence: "+ contents[0]+"\n");

            return ((new String(contents[0])).equals("SEQUENCE") ? ByteBuffer.wrap(contents[1]).getInt() : -1);
            
        } catch (IOException ex) {
            
            return -1;
        }
    }


    @Override
    public void replyReceived(TOMMessage tomm){
        View v = null;
        int s = -1;
        //System.out.println("received from sender: "+tomm.getSender()+"\n");
        byte[] bytes = tomm.getContent();
        if ((s = newSequence(tomm.getContent())) != -1) {
            System.out.println("receive sequence number: "+s+"\n");
        }
                
        //TODO: Need to be extended such that client will receive notice after it receives f+1 matching replies and no further messages for the same sequence number will be processed.
    }

    static private byte[][] deserializeContents(byte[] bytes) throws IOException {
        
        byte[][] batch = null;
        
        ByteArrayInputStream bis = new ByteArrayInputStream(bytes);
        DataInputStream in = new DataInputStream(bis);
        int nContents =  in.readInt();

        batch = new byte[nContents][];
        
        for (int i = 0; i < nContents; i++) {
            
            int length = in.readInt();

            batch[i] = new byte[length];
            in.read(batch[i]);
        }
        in.close();
        bis.close();

        return batch;
    }

    private class ReplyTuple {
        
        String channel;
        boolean config;
        
        ReplyTuple (String channel, boolean config) {
            this.channel = channel;
            this.config = config;
        }
    }
}