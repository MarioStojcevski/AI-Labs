using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Diagnostics;

namespace CSharp_Player
{
    class Program
    {
        static void Main(string[] args)
        {

            //System.Net.Sockets.TcpClient socket = new System.Net.Sockets.TcpClient();
            
            IPHostEntry ipHost = Dns.GetHostEntry("127.0.0.1");
            IPAddress ipAddr = ipHost.AddressList[0];
            IPEndPoint ipEndPoint = new IPEndPoint(ipAddr, 30000);
            Socket client = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            //client = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

            //Useful variables
            int gameEnd = 0;
            int maxTimeResponse = 5;

            // Player Name
            string playerName = "C# Player";

            // Connecting to the server
            try {
                //socket.Connect(HOST, PORT);
                client.Connect(ipEndPoint);
            } catch (Exception e) {
                Console.WriteLine("Error when connecting to the server!");
            }

            byte[] data = new byte[128];

            //Start of the game
            while (gameEnd == 0){

                Stopwatch elapsedTime = new Stopwatch();
                elapsedTime.Start();
                TimeSpan ts = elapsedTime.Elapsed;
                while (client.Available == 0 && ts.Seconds <= maxTimeResponse){
                    ts = elapsedTime.Elapsed;
                }

                if (client.Available > 0)
                    client.Receive(data);
                else {
                    Console.WriteLine("No response in {0} sec\n", maxTimeResponse);
                    gameEnd = 1;
                }
                string dataString = System.Text.Encoding.Default.GetString(data);
                if (dataString[0] == 'N'){
                    //TODO: send player name
                    byte[] msg = System.Text.Encoding.Default.GetBytes(playerName);
                    client.Send(msg);
                }

                if (dataString[0] == 'E')
                {
                    gameEnd = 1;
                }

                if (dataString[0] != 'N' && dataString[0] != 'E') {
                    //TODO: Transform the board and the playerTurn.
                    int playerTurn = dataString[0] -48;
                    Console.WriteLine(playerTurn);
                    int[] board = new int[14];

                    int i = 0;
                    int j = 1;
                    while (i <= 13)
                    {
                        board[i] = (dataString[j]-48) * 10 + (dataString[j + 1]-48);
                        i = i + 1;
                        j = j + 2;
                    }

                    //Using your intelligent bot, assign a move to "move".

                    // example: move = "1"; Possible moves from "1" to "6" if the game's 
                    // rules allows those moves.

                    //////////////// TODO: Change this ////////////////////
                    string move = "0";
                    ///////////////////////////////////////////////////////
                    
                    byte[] msg = System.Text.Encoding.Default.GetBytes(move);
                    client.Send(msg);
                }


            }
            Console.WriteLine("End of the game");
            client.Close();
        }
    }
}
