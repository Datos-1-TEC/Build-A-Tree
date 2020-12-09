package cr.ac.tec.JavaServer.TokensPrototype;

public class Triangle implements Token{
    private String shape = "Triangle";
    private int value;
    private int points = 30; 

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

    @Override
    public Integer getPoints() {
        return this.points;
    }
    
}
