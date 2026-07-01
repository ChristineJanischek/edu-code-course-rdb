import { initAssistantController } from "./controllers/assistant.controller.mjs";
import { initExerciseEvaluatorControllers } from "./controllers/exercise-evaluator.controller.mjs";
import { initKeywordIndexController } from "./controllers/keyword-index.controller.mjs";
import { initNavigationController } from "./controllers/navigation.controller.mjs";
import { initSubmissionController } from "./controllers/submission.controller.mjs";

initSubmissionController();
initAssistantController();
initKeywordIndexController();
initExerciseEvaluatorControllers();
initNavigationController();
