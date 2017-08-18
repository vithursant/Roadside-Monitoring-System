package main;

import java.awt.EventQueue;

import gui.SpeedSign;

public class Main {

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					SpeedSign speedsign = new SpeedSign();
					speedsign.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
}










































