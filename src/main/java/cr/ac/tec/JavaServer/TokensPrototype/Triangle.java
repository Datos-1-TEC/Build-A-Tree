package cr.ac.tec.JavaServer.TokensPrototype;
/**
 * Token tipo triagulo destinado para el reto de Splay
 * tiene un valor de 20 puntos
 * @author Juan Peña 
 */
public class Triangle implements Token{
    private String shape = "Triangle";
    private int value;
    private int points = 30; 

    public Triangle (){
        
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
