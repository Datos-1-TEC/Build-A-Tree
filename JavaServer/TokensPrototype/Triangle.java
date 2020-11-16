package JavaServer.TokensPrototype;

public class Triangle implements Token{
    private String shape = "Triangle";
    private int value;

    public Triangle (){
        System.out.println("Triangle token created");
    }

    @Override
    public Token makeToken() {
        Triangle triangleToken = null;

        try {
            triangleToken = (Triangle) super.clone();
        } catch (CloneNotSupportedException e) {
           
            e.printStackTrace();
        }
        
        return triangleToken;
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
