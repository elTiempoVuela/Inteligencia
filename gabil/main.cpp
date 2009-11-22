#include "gabil.h"
#include <sys/stat.h>
#include <fstream>

using namespace std;

int main(int argc, char **argv) {
  hypothesis_t *fittest;
  population_t *population;
  struct stat results;
  int size;
  float best_fitness = 0.;
  int it = 0;
 
  srand(time(NULL));
 
  
  // read file, parsed if possible.
  if (stat("data/adult.bin", &results) == 0){
    size = results.st_size/sizeof(long);
  }
  else{}
    // An error occurred
  ifstream file("data/adult.bin", ios::in | ios::binary);
  long * creprs = new long[size];

  file.read((char*)creprs,sizeof(long)*size);
  file.close();

  population = new population_t(creprs, size);

  fittest = population->get_fittest();

  cout << "Individuo " << fittest->rules[0]->p1_ << " " << fittest->rules[0]->p2_ << endl;
  cout << "Ejemplos " << endl << creprs[0] << " " << creprs[1] << endl << creprs[2] << " " << creprs[3] << endl;

  cout << "Fitness: " << fittest->fitness << endl;

//   while (true) { // dont know which stop condition =S
//     cout << "Generando poblacion " << ++it << endl;
//     fittest = population->get_fittest();
//     if (fittest->fitness > best_fitness)
//       best_fitness = fittest->fitness;

//     cout << "    Fitness:     " << (float)fittest->fitness * 100 << " %%" << endl;
//     cout << "    Best so far: " << (float)best_fitness * 100 << " %%" << endl;
//  }
}