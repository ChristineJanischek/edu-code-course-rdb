import { initCourseWorkflowController } from "./controllers/course-workflow.controller.mjs";
import { initExerciseEvaluatorControllers } from "./controllers/exercise-evaluator.controller.mjs";
import { initKeywordIndexController } from "./controllers/keyword-index.controller.mjs";
import { initNavigationController } from "./controllers/navigation.controller.mjs";
import { initPracticeFilesController } from "./controllers/practice-files.controller.mjs";
import { initSelfCheckController } from "./controllers/self-check.controller.mjs";
import { initTabsController } from "./controllers/tabs.controller.mjs";

initTabsController();
initCourseWorkflowController();
initPracticeFilesController();
initSelfCheckController();
initKeywordIndexController();
initExerciseEvaluatorControllers();
initNavigationController();
