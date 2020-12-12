package cr.ac.tec.JavaServer.TokensPrototype;

/**
 * Token tipo circulo destinado para el reto de AVL
 * tiene un valor de 20 puntos
 * @author Juan Peña
 */
public class Circle implements Token {
    private String shape = "Circle";
    private int value;
    private int points = 20;

    public Circle (){
    }

    @Override
    public Token makeToken() {
        Circle circleToken = null;

        try {
            circleToken = (Circle) super.clone();
        } catch (CloneNotSupportedException e) {
           
            e.printStackTrace();
        }
        
        return circleToken;
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
