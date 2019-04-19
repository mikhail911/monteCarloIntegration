#define PI 3.1415926535897932384626433832795

boolean do_your_job = true;
float xmin = 0;
float xmax = 0.5;
float ymin = 0;
float expected_value = 0.65757337; // only if expected value is known
unsigned long N = 100;
unsigned long t_start, t_end;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(0));
}

void loop() {
  if (do_your_job == true) {
    for (N; N <= 3000; N = N + 200) {
      monte_carlo(xmin, xmax, ymin, N);
    }
    do_your_job = false;
  }
}

float integral_function(float x) {
  /*
     1) func = sqrt(1 - pow(x, 2)); xmin = -1, xmax = 1, ymin = 0
     2) func = exp(x) * pow(cos(x), 2); xmin = 0, xmax = PI, ymin = 0
     3) func = sqrt((1 + x) / (1 - x)); xmin = 0, xmax = 0.5, ymin = 0
  */
  float func = sqrt((1 + x) / (1 - x));
  return func;
}

float find_ymax(float xmin, float xmax) {
  int precision = 1000;
  float temp[precision + 1];
  float step_val = (xmax - xmin) / precision;
  float max_val = 0;
  // create array with y values of function
  for (int i = 0; i < precision + 1; i++) {
    temp[i] = integral_function(i * step_val);
    // find max value of y array
    if (temp[i] > max_val) {
      max_val = temp[i];
    }
  }
  return max_val;
}

void monte_carlo(float xmin, float xmax, float ymin, unsigned long N) {
  float ymax = find_ymax(xmin, xmax);
  float whole_area = (xmax - xmin) * (ymax - ymin);
  unsigned long hit_points = 0;
  float result = 0;
  t_start = millis();

  for (unsigned long i = 0; i < N; i++) {
    float x = xmin + (xmax - xmin) * ((float)random(0, 100) / 100);
    float y = ymin + (ymax - ymin) * ((float)random(0, 100) / 100);

    if (y > ymin && y <= integral_function(x)) { //zamienic na 0 -> ymin
      hit_points = hit_points + 1;
    }
  }
  t_end = millis();
  result = (whole_area * hit_points) / N;
  Serial.println("------");
  Serial.print("Result: ");
  Serial.println(result, 8);
  Serial.print("Total time: ");
  Serial.println(t_end - t_start);
  Serial.print("N: ");
  Serial.println(N);
  if (expected_value > 0) {
    // For PI: abs_error = expected_value - 2 * result
    float abs_error = expected_value - result;
    Serial.print("Abs error: ");
    Serial.println(abs(abs_error), 8);
    Serial.print("Rel error [%]: ");
    Serial.println((abs_error / expected_value) * 100, 8);
  }
}
