package cr.ac.tec.JavaServer.TokensPrototype;

public interface Token extends Cloneable{
    
    public Token makeToken();
    public String getShape();
    public Integer getValue ();
    public void setValue (int value);
}
