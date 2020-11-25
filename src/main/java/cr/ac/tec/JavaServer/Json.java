package cr.ac.tec.JavaServer;

import com.fasterxml.jackson.core.JsonProcessingException;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Clase que maneja los archivos de tipo Json, así como su escritura
 */
public class Json {
    private static ObjectMapper objectMapper = getDefaultObjectMapper();

    /**
     * metodo de estructura Singleton utilizado para obtener la instancia ObjectMapper
     * @return defaultObjectMapper
     */
    private static ObjectMapper getDefaultObjectMapper() {
        ObjectMapper defaultObjectMapper = new ObjectMapper();
        return defaultObjectMapper;
    }

    /**
     * Metodo que traduce un string a un JsonNode
     * @param jsonSource string a ser traducido
     * @return JsonNode
     * @throws JsonProcessingException
     */
    public static JsonNode parse(String jsonSource) throws JsonProcessingException {
        return objectMapper.readTree(jsonSource);
    }

    /**
     * Metodo que pasa un Objeto a JsonNode
     * @param o
     * @return
     */
    public static JsonNode toJson (Object o){ return objectMapper.valueToTree(o);}

    /**
     * Metodo que toma un JsonNode y lo pasa a una clase especificada
     * @param node Nodo que será convertido
     * @param aClass Clase esperada
     * @param <A> Parametro Genérico para incluir cualquier tipo de clase
     * @return clase especificada
     * @throws JsonProcessingException
     */
    public static <A> A fromJson( JsonNode node, Class<A> aClass) throws JsonProcessingException {
        return objectMapper.treeToValue(node, aClass);
    }

    /**
     * Metodo que genera un String de formato Json
     * @param node nodo a convertir en String
     * @param pretty boolean para dar formato
     * @return String formateado
     * @throws JsonProcessingException
     */
    public static String generateString (JsonNode node, boolean pretty) throws JsonProcessingException{
        ObjectWriter objectWriter = objectMapper.writer();
        if(pretty){
            objectWriter = objectWriter.with(SerializationFeature.INDENT_OUTPUT);
        }
        return objectWriter.writeValueAsString(node);
    }

    public String jsonReader (String json, String fileName) throws IOException {
        // Read the file
        BufferedReader br = new BufferedReader(new FileReader(fileName));
        try {
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();
            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = br.readLine();
            }
            json = sb.toString();
        } finally {
            br.close();
        }
        return json;
    }

}
