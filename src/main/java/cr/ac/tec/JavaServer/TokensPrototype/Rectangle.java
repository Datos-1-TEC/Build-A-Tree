package cr.ac.tec.JavaServer.TokensPrototype;

public class Rectangle implements Token {
    private String shape = "Rectangle";
    private int value;
    private int points = 40;

    public Rectangle() {
        System.out.println("Rectangle token created");
    }

    @Override
    public Token makeToken() {

        Rectangle recToken = null;

        try {
            recToken = (Rectangle) super.clone();
        } catch (CloneNotSupportedException e) {
           
            e.printStackTrace();
        }
        
        return recToken;
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
