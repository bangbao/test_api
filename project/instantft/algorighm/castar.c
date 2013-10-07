#include <stdlib.h>
#include <stdio.h>
#ifdef __APPLE__
#include "sys/malloc.h"
#else
#include <malloc.h>
#endif
#include <Python.h>

#define IS_NULL(value) (value == NULL ? true : false)
#define BINT_CHUNK_SIZE 31
#define P1 0
#define P3 1
#define P5 3
#define P6 4
#define P7 5
#define P9 6
#define P11 7
#define P12 8

typedef unsigned int uint;
typedef enum {false, true} bool;
typedef struct NodeStatus {
  uint f;
  uint h;
  uint g;
  uint pos;
  bool open;
  bool valid;
  struct NodeStatus *parent;
  struct NodeStatus *next;
  struct NodeStatus *qnext;
} NodeStatus;

typedef struct Path {
  struct NodeStatus *start;
  struct NodeStatus *best;
} Path;

typedef struct BInt {
  uint *value;
  uint len;
} bint_array;

inline div_t bint_hash(uint value) {
  return div(value, BINT_CHUNK_SIZE);
}

inline bool bint_search(bint_array *bint, uint value) {
  div_t pos = bint_hash(value);

  if ((value < 0) || pos.quot > bint->len) {
    return false;
  }

  return bint->value[pos.quot] & (1 << pos.rem) ? true : false;
}

bint_array *create_bint(uint len, uint *init, uint init_len) {
  div_t pos;
  uint i;
  div_t dsize = div(len, BINT_CHUNK_SIZE);
  bint_array *bint = malloc(sizeof(bint_array));
  bint->value = NULL;
  bint->len = dsize.quot;

  if (dsize.rem) {
    bint->len += 1;
  }

  uint *values = malloc(bint->len * sizeof(uint));
  memset(values, 0, (bint->len * sizeof(uint)));

  for (i = 0; i < init_len; i++) {
    pos = bint_hash(init[i]);
    values[pos.quot] |= 1 << pos.rem;
  }

  bint->value = values;
  
  return bint;
}

inline int heuristic(uint pos, uint goal, uint len) {
  div_t d1 = div(goal, len);
  div_t d2 = div(pos, len);

  return abs(d2.quot - d1.quot) + abs(d2.rem - d1.rem);
}

inline uint pos_cost(uint pos, uint goal) {
   return 2;
}

void dump_arrays(int *array, uint len) {
  int i;

  printf("dump array");

  for (i = 0; i < len; i++) {
    printf("  %d", *array);
    array++;
  }
  printf("\n");
}

int *neighbors(uint pos, uint len, uint max_value, const bint_array *bint) {
  static int positions[] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  bool realness[] =  {false, false, false, false, false, false, false, false};
  int posrow = pos / len;
  uint i;

  positions[P3] = pos + 1;
  positions[P5] = positions[P3] + len;
  positions[P6] = positions[P5] - 1;
  positions[P7] = positions[P6] - 1;
  positions[P9] = positions[P7] - len;
  positions[P11] = positions[P9] - len;
  positions[P12] = positions[P11] + 1;
  positions[P1] = positions[P12] + 1;
   
  if (positions[P3] / len == posrow) {
    realness[P3] = true;
    realness[P5] = positions[P5] < max_value ? true : false;
    realness[P1] = positions[P1] >= 0 ? true : false;
  }

  if (positions[P9] / len == posrow) {
    realness[P9] = true;
    realness[P11] = positions[P11] >= 0 ? true : false;
    realness[P7] = positions[P7] < max_value ? true: false;
  }

  realness[P6] = positions[P6] < max_value ? true : false;
  realness[P12] = positions[P12] >= 0 ? true : false;

  for (i = 0; i < 8; i++) {
    if (!realness[i] || bint_search(bint, positions[i])) {
      positions[i] = -1;
    }
  }
  
  return positions;
}

NodeStatus *get_node(uint pos, NodeStatus *start) {
  NodeStatus *current = start;

  while (!IS_NULL(current)) {
    if (current->pos == pos) {
      return current;
    }
    current = current->next;
  }

  return NULL;
}

Path *_castar(uint start_pos, uint goal_pos, uint start_g, uint len, uint max_value, const bint_array *bint) {
  uint start_h = heuristic(start_g, goal_pos, len);
  uint neighbor_g = 0;
  uint neighbor_h = 0;
  uint i;

  NodeStatus *start = malloc(sizeof(NodeStatus));
  start->f = start_g + start_h;
  start->h = start_h;
  start->g = start_g;
  start->pos = start_pos;
  start->open = true;
  start->valid = true;
  start->parent = NULL;
  start->next = NULL;
  start->qnext = NULL;

  NodeStatus *last = start;
  NodeStatus *best = start;
  NodeStatus *heap = start;
  NodeStatus *qlast = start;
  NodeStatus *current = NULL;
  NodeStatus *neighbor = NULL;
  Path *path = malloc(sizeof(Path));

  path->start = start;

  while (!IS_NULL(heap)) {
    current = heap;
    heap = current->qnext;
    current->qnext = NULL;

    if (current->pos == goal_pos) {
      break;
    }

    int *neighbor_list = neighbors(current->pos, len, max_value, bint);

    for (i = 0; i < 8; i++) {
      if (*neighbor_list < 0) {
	goto loop_next;
      }

      neighbor_g = current->g + pos_cost(current->pos, *neighbor_list);
      neighbor = get_node(*neighbor_list, start);

      if (IS_NULL(neighbor)) {
	NodeStatus *neighbor = malloc(sizeof(NodeStatus));

	neighbor_h = heuristic(*neighbor_list, goal_pos, len);
	neighbor->f = neighbor_g + neighbor_h;
	neighbor->h = neighbor_h;
	neighbor->g = neighbor_g;
	neighbor->pos = *neighbor_list;
	neighbor->open = true;
	neighbor->valid = true;
	neighbor->parent = current;
	neighbor->next = NULL;
	neighbor->qnext = NULL;

	last->next = neighbor;
	last = neighbor;

	if (IS_NULL(heap)) {
	  heap = neighbor;
	} else {
	  qlast->qnext = neighbor;
	}

	qlast = neighbor;

	if (neighbor_h < best->h) {
	  best = neighbor;
	}
      } else if (neighbor_g < neighbor->g) {
	if (neighbor->open) {
	  neighbor->valid = false;
	  neighbor->f = neighbor_g + neighbor->h;
	  neighbor->g = neighbor_g;
	  neighbor->valid = true;
	  neighbor->parent = current;
	} else {
	  neighbor->f = neighbor_g + neighbor->h;
	  neighbor->g = neighbor_g;
	  neighbor->parent = current;
	  neighbor->open = true;
	}

	if (IS_NULL(heap)) {
	  heap = neighbor;
	} else {
	  qlast->qnext = neighbor;
	}

	qlast = neighbor;
      }

    loop_next:
      neighbor_list++;
    }
  }

  path->best = best;

  return path;
}

static PyObject *shardfind(PyObject *self, PyObject *args) {
  uint start_pos;
  uint goal_pos;
  uint direction:2;
  uint distance;
  uint len;
  uint max_value;
  uint start_g;
  NodeStatus *node = NULL;
  NodeStatus *release = NULL;

  if (!PyArg_ParseTuple(args, "i|i|i|i|i|i", &start_pos, &goal_pos, &len,
			&max_value, &start_g, &distance))
    return NULL
}

static PyObject *
pycastar(PyObject *self, PyObject *args) {
  uint start_pos;
  uint goal_pos;
  uint len;
  uint start_g;
  uint max_value;
  NodeStatus *node = NULL;
  NodeStatus *release = NULL;
  bint_array *bint = NULL;
  PyListObject *pblocks;
  PyObject *blocks;
  PyObject *value;

  uint init_len = 0;
  uint i;

  if (!PyArg_ParseTuple(args, "i|i|i|i|i|O!", &start_pos, &goal_pos,
			&len, &max_value, &start_g, &PyDict_Type, &blocks))
        return NULL;

  pblocks = PyDict_Values(blocks);
  init_len = (uint)PyList_GET_SIZE(pblocks);
  uint *init = malloc(init_len * sizeof(uint));
  memset(init, 0, (init_len * sizeof(uint)));

  for (i = 0; i < init_len; i++) {
    value = PyList_GetItem(pblocks, i);
    init[i] = (uint)PyInt_AsLong(value);
  }

  bint = create_bint(max_value, init, init_len);
  free(init);

  Path *path = _castar(start_pos, goal_pos, start_g, len, max_value, bint);
  PyObject *line = PyList_New(0);

  node = path->best;

  while (!IS_NULL(node->parent)) {
    PyList_Append(line, PyInt_FromLong(node->pos));
    node = node->parent;
  }

  node = path->start;

  while (!IS_NULL(node)) {
    release = node;
    node = node->next;

    free(release);
  }

  free(path);
  free(bint->value);
  free(bint);

  Py_INCREF(line);

  return line;
}

static PyMethodDef cAstarMethods[] = {
    {"pycastar",  pycastar, METH_VARARGS,
     "Aastar path find c version."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initcastar(void)
{
  (void) Py_InitModule("castar", cAstarMethods);
}

/* int main(void) { */
/*   uint start_pos = 1; */
/*   uint goal_pos = 134; */
/*   uint len = 30; */
/*   uint start_g = 1; */
/*   uint max_value = 600; */
/*   NodeStatus *node = NULL; */
/*   NodeStatus *release = NULL; */

/*   Path *path = _castar(start_pos, goal_pos, start_g, len, max_value, ); */

/*   node = path->best; */

/*   while (!IS_NULL(node->parent)) { */
/*     node = node->parent; */
/*   } */

/*   node = path->best; */

/*   while (!IS_NULL(node)) { */
/*     release = node; */
/*     node = node->next; */

/*     free(release); */
/*   } */

/*   free(path); */

/*   return 0; */
/* } */
