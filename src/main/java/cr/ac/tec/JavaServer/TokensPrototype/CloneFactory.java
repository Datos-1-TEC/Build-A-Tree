package cr.ac.tec.JavaServer.TokensPrototype;
/** Esta clase interactúa con un determinado cliente que requiere instancias de diferentes tokens 
 * para asignarlos como nodos para un tipo de árbol
 * @author Juan P.R
 */
public class CloneFactory {
    /**Este método se encarga de clonar el objeto que se le pida desde el cliente
     * @param recibe un tipo de token que se desea clonar
     * @return retorna el token clonado mediante el método makeToken() de la interface Token
     */
    public Token getToken(Token tokenSample){

        return tokenSample.makeToken();

    }
}
