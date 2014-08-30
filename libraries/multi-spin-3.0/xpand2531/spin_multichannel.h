#ifndef XPANSPIN_H
#define XPANSPIN_H

//number of nodes of which the network is composed
#define MAX_NUM_NODES 2
#define SPIN_HOLE 0x7F //127 (max of signed 8 bit)

//content of the packets transmitted by the nodes
//the packet counter is a 16-bit counter (each packet has a unique value)
typedef struct {
  unsigned int packet_counter;
  char TX_id;
  signed char RSS[MAX_NUM_NODES];
  signed char TX_channel;
} spinPacket_t;

#endif
