package gui;

import javax.swing.JFrame;
import javax.swing.UIManager;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;

import com.fazecast.jSerialComm.SerialPort;

import net.miginfocom.swing.MigLayout;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.util.Scanner;
import java.awt.event.ActionEvent;
import javax.swing.JComboBox;
import javax.swing.JTextPane;
import java.awt.Font;
import javax.swing.JTextField;
import java.awt.Color;
import javax.swing.SwingConstants;
import javax.swing.JTextArea;

public class SpeedSign {

	public JFrame frame;
	static SerialPort port;
	private JTextField textField;
	private JTextField txtWarning;
	private JTextField textField_1;
	
	private final String WARNING = "CAUTION: ROAD WORKERS AHEAD";
	private final String ROADS_CLEAR = "DRIVE SAFE NO WORKERS PRESENT";

	/**
	 * Create the application.
	 */
	public SpeedSign() {
		try {
			UIManager.setLookAndFeel("javax.swing.plaf.nimbus.NimbusLookAndFeel");
		} catch (Exception e){
			e.printStackTrace();
		}
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.setBounds(100, 100, 1920, 1080);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(new MigLayout("", "[81.00][525.00,grow][431.00,grow][149.00][493.00,grow][70.00]", "[][][][][223.00][186.00][160.00][189.00][grow]"));
		
		JComboBox<String> portList = new JComboBox<String>();
		frame.getContentPane().add(portList, "cell 2 1,growx");
		
		JTextPane textPane = new JTextPane();
		textPane.setEditable(false);
		textPane.setFont(new Font("Tahoma", Font.PLAIN, 200));
		frame.getContentPane().add(textPane, "cell 2 4 2 3,grow");
		
		StyledDocument doc = textPane.getStyledDocument();
		SimpleAttributeSet center = new SimpleAttributeSet();
		StyleConstants.setAlignment(center, StyleConstants.ALIGN_CENTER);
		doc.setParagraphAttributes(0, doc.getLength(), center, false);
		
		// add port names to combo box
		SerialPort[] portNames = SerialPort.getCommPorts();
		for(int i = 0; i < portNames.length; i++)
			portList.addItem(portNames[i].getSystemPortName());
		
		JTextPane txtpnSpeedLimit = new JTextPane();
		txtpnSpeedLimit.setFont(new Font("Tahoma", Font.BOLD, 50));
		txtpnSpeedLimit.setText("SPEED LIMIT");
		frame.getContentPane().add(txtpnSpeedLimit, "cell 2 3 2 1,grow");
		
		doc = txtpnSpeedLimit.getStyledDocument();
		StyleConstants.setAlignment(center, StyleConstants.ALIGN_CENTER);
		doc.setParagraphAttributes(0, doc.getLength(), center, false);
		
		textField_1 = new JTextField(ROADS_CLEAR);
		textField_1.setHorizontalAlignment(SwingConstants.CENTER);
		textField_1.setFont(new Font("Tahoma", Font.PLAIN, 90));
		textField_1.setForeground(Color.BLACK);
		textField_1.setEditable(false);
		frame.getContentPane().add(textField_1, "cell 1 7 4 1,growx");
		textField_1.setColumns(10);
		
		JButton btnConnect = new JButton("Connect");
		btnConnect.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {

				if(btnConnect.getText().equals("Connect")) {
					// attempt to connect to the serial port
					port = SerialPort.getCommPort(portList.getSelectedItem().toString());
					port.setComPortTimeouts(SerialPort.TIMEOUT_SCANNER, 0, 0);
					if(port.openPort()) {
						btnConnect.setText("Disconnect");
						portList.setEnabled(false);
					}
					
					Thread thread = new Thread(){
						@Override public void run() {
							Scanner scanner = new Scanner(port.getInputStream());
							while(scanner.hasNextLine()) {
								try {
									String line = scanner.nextLine();
									System.out.println(line);
									textPane.setText(line+"\nKM/H");
									if(Integer.parseInt(line) <= 90) {
										textField_1.setText(WARNING);
										textField_1.setForeground(Color.RED);
									}
									else {
										textField_1.setText(ROADS_CLEAR);
										textField_1.setForeground(Color.BLACK);
									}
								} catch(Exception e) {}
							}
							scanner.close();
						}
					};
					thread.start();
				} else {
					// disconnect from the serial port
					if(port.isOpen()) {
						port.closePort();
						portList.setEnabled(true);
						btnConnect.setText("Connect");
					}
				}
			}
		});
		frame.getContentPane().add(btnConnect, "cell 3 1");

	}
}
