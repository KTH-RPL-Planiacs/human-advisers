import py4j.GatewayServer;

public class PrismEntryPoint {

	private PrismHandler handler;
	
	public PrismEntryPoint() {
		handler = new PrismHandler();
	}
	
	public PrismHandler getPrismHandler() {
		return handler;
	}
	
	public static void main(String[] args) {
		GatewayServer gatewayServer = new GatewayServer(new PrismEntryPoint());
		gatewayServer.start();
		System.out.println("Gateway Server Started");
    }
}

