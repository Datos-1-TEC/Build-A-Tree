package JavaServer.TokensPrototype;

public class Diamond implements Token{
    private String shape = "Diamond";
    private int value;

    public Diamond(){
        System.out.println("Diamond token created");

    }

    @Override
    public Token makeToken() {
        Diamond diamondToken = null;

        try {
            diamondToken = (Diamond) super.clone();
        } catch (CloneNotSupportedException e) {
           
            e.printStackTrace();
        }
        
        return diamondToken;
    }

    @Override
    public String getShape() {
        return this.shape;
    }

    @Override
    public Integer getValue() {

        return this.value;
    }

    @Override
    public void setValue(int value) {
        this.value = value;
    }
    
}
