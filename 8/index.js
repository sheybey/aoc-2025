const { mat4, quat } = glMatrix;

async function sleep(ms) {
  return new Promise((resolve) => {
    window.setTimeout(() => resolve, ms);
  });
}

/**
 * @typedef {[number, number, number]} Point
 */

/**
 * @param {Point} p1
 * @param {Point} p2
 */
function distance(p1, p2) {
  const [x1, y1, z1] = p1;
  const [x2, y2, z2] = p2;
  return Math.sqrt(
    Math.pow((x2 - x1), 2) +
    Math.pow((y2 - y1), 2) +
    Math.pow((z2 - z1), 2)
    );
}

/**
 * @param {Point[]} a
 * @returns {Generator<[Point, Point], any, any>}
 */
function* combinations(a) {
  for (let i = 0; i < a.length-1; i += 1) {
    for (let j = i+1; j < a.length; j += 1) {
      yield [a[i], a[j]];
    }
  }
}

/** @type {Point[]} */
const points = [];

let min_dimension = Infinity;
let max_dimension = -Infinity;

/** @type {string} */
let input;
if (typeof process === 'undefined') {
  const file = await fetch('./input');
  input = await file.text();
} else {
  const fs = await import('node:fs/promises');
  input = await fs.readFile('./input', { encoding: 'utf8' });
}

for (const line of input.trim().split('\n')) {
  const point = line.split(',').map((n) => parseInt(n.trim(), 10))
  min_dimension = Math.min(min_dimension, ...point);
  max_dimension = Math.max(max_dimension, ...point);
  points.push(point);
}

const pairs = Array.from(combinations(points));

const canvas = document.createElement('canvas');
document.body.appendChild(canvas);

function resize([current,]) {
  let width;
  let height;
  let dpr = window.devicePixelRatio;
  if (current.devicePixelContentBoxSize) {
    // NOTE: Only this path gives the correct answer
    // The other paths are an imperfect fallback
    // for browsers that don't provide anyway to do this
    width = current.devicePixelContentBoxSize[0].inlineSize;
    height = current.devicePixelContentBoxSize[0].blockSize;
    dpr = 1; // it's already in width and height
  } else if (current.contentBoxSize) {
    if (current.contentBoxSize[0]) {
      width = current.contentBoxSize[0].inlineSize;
      height = current.contentBoxSize[0].blockSize;
    } else {
      // legacy
      width = current.contentBoxSize.inlineSize;
      height = current.contentBoxSize.blockSize;
    }
  } else {
    // legacy
    width = current.contentRect.width;
    height = current.contentRect.height;
  }
  canvas.width = Math.round(width * dpr);
  canvas.height = Math.round(height * dpr);
}
const observer = new ResizeObserver(resize);
observer.observe(canvas, { box: 'content-box' });

let ctx = canvas.getContext('webgl2');

class ShaderCompileException extends Error {
  constructor(shader) {
    if (typeof shader === 'string') {
      super(shader)
    } else {
      let message = ctx.getShaderInfoLog(shader);
      super('An error occurred while compiling the shader:\n' + message);
      this.glMessage = message;
      this.src = ctx.getShaderSource(shader);
      ctx.deleteShader(shader);
    }
  }
}

function loadShader(type, source) {
  // Compile the shader program
  const shader = ctx.createShader(type);
  ctx.shaderSource(shader, source);
  ctx.compileShader(shader);

  // See if it compiled successfully
  if (!ctx.getShaderParameter(shader, ctx.COMPILE_STATUS)) {
    throw new ShaderCompileException(shader);
  }

  return shader;
};


class ShaderProgram {
  constructor(vertexSource, fragmentSource) {
    const vertex = loadShader(ctx.VERTEX_SHADER, vertexSource);
    const fragment = loadShader(ctx.FRAGMENT_SHADER, fragmentSource);

    this.program = ctx.createProgram();
    ctx.attachShader(this.program, vertex);
    ctx.attachShader(this.program, fragment);
    ctx.linkProgram(this.program);

    ctx.deleteShader(vertex);
    ctx.deleteShader(fragment);

    if (!ctx.getProgramParameter(this.program, ctx.LINK_STATUS)) {
      throw new ShaderCompileException(
        `Unable to initialize the shader program: ${ctx.getProgramInfoLog(
          this.program,
        )}`,
      );
    }

    this.vertexPos = ctx.getAttribLocation(this.program, 'aVertexPosition');
    this.vertexBuf = ctx.createBuffer();
    this.projection = ctx.getUniformLocation(this.program, 'uProjectionMatrix');
    this.modelView = ctx.getUniformLocation(this.program, 'uModelViewMatrix');
  }

  setVertices(vertices) {
    ctx.bindBuffer(ctx.ARRAY_BUFFER, this.vertexBuf);
    ctx.bufferData(ctx.ARRAY_BUFFER, new Float32Array(vertices), ctx.STATIC_DRAW);
  }

  enable() {
    ctx.useProgram(this.program);
    ctx.bindBuffer(ctx.ARRAY_BUFFER, this.vertexBuf);
    const numComponents = 3; // pull out 3 values per iteration
    const type = ctx.FLOAT; // the data in the buffer is 32bit floats
    const normalize = false; // don't normalize
    const stride = 0; // how many bytes to get from one set of values to the next
    // 0 = use type and numComponents above
    const offset = 0; // how many bytes inside the buffer to start from
    ctx.vertexAttribPointer(
      this.vertexPos,
      numComponents,
      type,
      normalize,
      stride,
      offset,
    );
    ctx.enableVertexAttribArray(this.vertexPos);
  }

  disable() {
    ctx.disableVertexAttribArray(this.vertexPos);
  }
}

/**
 * @param {Point[]} vertices
 */
function normalizeVertices(vertices) {
    let range = max_dimension - min_dimension;
    range /= 2;
    return vertices.flatMap((p) => p.map((c) => 1-((c-min_dimension)/range)));
}

class PointProgram extends ShaderProgram {
  constructor() {
    super(
      `
      attribute vec4 aVertexPosition;
      uniform mat4 uModelViewMatrix;
      uniform mat4 uProjectionMatrix;

      void main(void) {
        gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
      }
      `, `
      void main(void) {
        gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
      }
      `
    );
    super.setVertices(normalizeVertices(points));
  }

  draw(projection, modelView) {
    this.enable();

    ctx.uniformMatrix4fv(this.projection, false, projection);
    ctx.uniformMatrix4fv(this.modelView, false, modelView);

    ctx.drawArrays(ctx.POINTS, 0, points.length);

    this.disable();
  }
}

class ConnectionProgram extends ShaderProgram {
  constructor() {
    super(
      `
        attribute vec4 aVertexPosition;
        uniform mat4 uModelViewMatrix;
        uniform mat4 uProjectionMatrix;
        
        attribute highp float aVertexAge;
        uniform highp float uTotal;

        varying highp vec3 color;

        void main(void) {
          gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
          // green to red based on how old this connection is
          float pct = float(aVertexAge) / float(uTotal);
          color = vec3(pct, 1.0-pct, 0.0);
        }
      `, `
        varying highp vec3 color;

        void main(void) {
          gl_FragColor = vec4(color, 1.0);
        }
      `
    );

    debugger;
    super.setVertices(normalizeVertices(pairs.flatMap((p) => p)));
    this.connections = 0;

    this.ages = pairs.flatMap(() => [0, 0]);
    this.agePos = ctx.getAttribLocation(this.program, 'aVertexAge');
    this.ageBuf = ctx.createBuffer();

    ctx.bindBuffer(ctx.ARRAY_BUFFER, this.ageBuf);
    ctx.bufferData(ctx.ARRAY_BUFFER, new Float32Array(this.ages), ctx.DYNAMIC_DRAW);

    this.total = ctx.getUniformLocation(this.program, 'uTotal');
  }

  increment() {
    ctx.useProgram(this.Program);
    this.connections += 1;
    for (let i = 0; i < this.connections; i += 1) {
      let j = 2*i;
      this.ages[j] += 1;
      this.ages[j+1] += 1;
    }
    ctx.bindBuffer(ctx.ARRAY_BUFFER, this.ageBuf);
    const updated = new Float32Array(this.ages.slice(this.connections * 2));
    ctx.bufferSubData(ctx.ARRAY_BUFFER, 0, updated);
  }

  enable() {
    super.enable();
    ctx.uniform1f(this.total, this.connections);
    ctx.bindBuffer(ctx.ARRAY_BUFFER, this.ageBuf);
    const numComponents = 1; // pull out 1 value per iteration
    const type = ctx.FLOAT; // the data in the buffer is 32bit floats
    const normalize = false; // don't normalize
    const stride = 0; // how many bytes to get from one set of values to the next
    // 0 = use type and numComponents above
    const offset = 0; // how many bytes inside the buffer to start from
    ctx.vertexAttribPointer(
      this.agePos,
      numComponents,
      type,
      normalize,
      stride,
      offset,
    );
    ctx.enableVertexAttribArray(this.agePos);
  }

  disable() {
    super.disable();
    ctx.disableVertexAttribArray(this.agePos);
  }

  draw(projection, modelView) {
    this.enable();

    ctx.uniformMatrix4fv(this.projection, false, projection);
    ctx.uniformMatrix4fv(this.modelView, false, modelView);

    ctx.drawArrays(ctx.LINES, 0, this.connections);

    this.disable();
  }
}

let pitch = 0;
let yaw = 0;

function toRad(degrees) {
  return (degrees * Math.PI) / 180;
}

const pointProgram = new PointProgram();
const connectionProgram = new ConnectionProgram();

function draw() {
  ctx.viewport(0, 0, ctx.canvas.width, ctx.canvas.height);
  ctx.clearColor(0x1c/255, 0x1b/255, 0x22/255, 1.0); // Clear to gray, fully opaque
  ctx.clearDepth(1.0); // Clear everything
  ctx.enable(ctx.DEPTH_TEST); // Enable depth testing
  ctx.depthFunc(ctx.LEQUAL); // Near things obscure far things

  // Clear the canvas before we start drawing on it.
  ctx.clear(ctx.COLOR_BUFFER_BIT | ctx.DEPTH_BUFFER_BIT);

  // Create a perspective matrix, a special matrix that is
  // used to simulate the distortion of perspective in a camera.
  // Our field of view is 45 degrees, with a width/height
  // ratio that matches the display size of the canvas
  // and we only want to see objects between 0.1 units
  // and 100 units away from the camera.
  const fieldOfView = toRad(45); // in radians
  const aspect = ctx.canvas.clientWidth / ctx.canvas.clientHeight;
  const zNear = 0.1;
  const zFar = 100.0;
  const projectionMatrix = mat4.create();

  // note: glMatrix always has the first argument
  // as the destination to receive the result.
  mat4.perspective(projectionMatrix, fieldOfView, aspect, zNear, zFar);

  // Set the drawing position to the "identity" point, which is
  // the center of the scene.
  const modelViewMatrix = mat4.create()

  // Now move the drawing position a bit to where we want to
  // start drawing the square.
  mat4.fromRotationTranslation(
    modelViewMatrix, // destination matrix
    quat.fromEuler(quat.create(), pitch, yaw, 0),
    [-0.0, 0.0, -5.0],
  );

  pointProgram.draw(projectionMatrix, modelViewMatrix);
  // connectionProgram.draw(projectionMatrix, modelViewMatrix);

  window.requestAnimationFrame(draw);
}

/**
 * @param {MouseEvent} event
 */
function applyRotation(event) {
  yaw += .5 * event.movementX;
  const newPitch = pitch + .5 * event.movementY;
  pitch = Math.min(90, Math.max(-90, newPitch));
}

window.addEventListener('mousedown', () => window.addEventListener('mousemove', applyRotation));
window.addEventListener('mouseup', () => window.removeEventListener('mousemove', applyRotation));
draw();

/**
 * @typedef
 * @param {Array<[Point, Point]>} connections
 * @param {Array<Set<Point>>} circuits
 * @returns {[Set<Point>[], ([Point, Point] | undefined)]}
 */
function connect(connections, circuits=[]) {
  for (const [p1, p2] of connections) {
    // connectionProgram.increment();
    // find all circuits that contain either junction box
    const contains = [];
    const others = [];
    for (const circuit of circuits) {
      if (circuit.has(p1) || circuit.has(p2)) {
        contains.push(circuit);
      } else {
        others.push(circuit);
      }
    }

    // combine all circuits that contain either box into a new circuit
    circuits = others;
    const new_circuit = new Set([p1, p2]);
    for (const circuit of contains) {
      for (const p of circuit) {
        new_circuit.add(p);
      }
    }
    circuits.push(new_circuit);

    // part 2 check
    if (circuits.length === 1 && circuits[0].size === points.length) {
      return [circuits, [p1, p2]];
    }
  }

  return [circuits, undefined];
}

pairs.sort((c1, c2) => distance(...c1) - distance(...c2));

let [circuits,] = connect(pairs.slice(0, 1000));
// const lengths = circuits.map((c) => c.size);
// lengths.sort((a, b) => b - a);
// console.log('part 1:', lengths[0] * lengths[1] * lengths[2]);

// let last;
// [circuits, last] = connect(pairs.slice(1000), circuits);
// if (last === undefined) {
//   console.log('failed to connect all circuits');
// } else {
//   console.log('part 2:', last, last[0][0] * last[1][0]);
// }
