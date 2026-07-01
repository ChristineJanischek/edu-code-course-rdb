import { initAssistantController } from "./controllers/assistant.controller.mjs";
import { initExerciseEvaluatorControllers } from "./controllers/exercise-evaluator.controller.mjs";
import { initKeywordIndexController } from "./controllers/keyword-index.controller.mjs";
import { initNavigationController } from "./controllers/navigation.controller.mjs";
import { initPracticeFilesController } from "./controllers/practice-files.controller.mjs";
import { initSelfCheckController } from "./controllers/self-check.controller.mjs";
import { initSubmissionController } from "./controllers/submission.controller.mjs";
import { initTabsController } from "./controllers/tabs.controller.mjs";

initTabsController();
initSubmissionController();
initAssistantController();
initPracticeFilesController();
initSelfCheckController();
initKeywordIndexController();
initExerciseEvaluatorControllers();
initNavigationController();
