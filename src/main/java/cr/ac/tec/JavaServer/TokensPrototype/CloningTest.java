package cr.ac.tec.JavaServer.TokensPrototype;


public class CloningTest {
    public static void main(String[] args){
        CloneFactory tokenMaker = new CloneFactory();
        Diamond bstToken = new Diamond();
        Diamond clonedDiamond = (Diamond)tokenMaker.getToken(bstToken);

        System.out.println(bstToken.getShape());
        System.out.println(clonedDiamond.getShape());


    }
}
