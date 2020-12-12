package cr.ac.tec.JavaServer.TokensPrototype;

/**
 * Token tipo rombo destinado para el reto de BST
 * tiene un valor de 15 puntos
 * @author Juan Peña
 */
public class Diamond implements Token{
    private String shape = "Diamond";
    private int value;
    private int points = 15;

    public Diamond(){
       
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

    @Override
    public Integer getPoints() {
        return this.points;
    }
    
}
