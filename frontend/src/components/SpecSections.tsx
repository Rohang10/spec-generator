/* eslint-disable @typescript-eslint/no-explicit-any */
import { motion, AnimatePresence } from "framer-motion";
import JsonViewer from "./JsonViewer";

export default function SpecSections({
  spec,
  activeTab,
}: {
  spec: any;
  activeTab: string;
}) {
  const contentMap: Record<string, any> = {
    "Modules & Features": {
      modules: spec.modules,
      features_by_module: spec.features_by_module,
    },
    "User Stories": spec.user_stories,
    "API Endpoints": spec.api_endpoints,
    "DB Schema": spec.db_schema,
    "Open Questions": spec.open_questions,
  };

  return (
    <div className="relative">
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -12 }}
          transition={{ duration: 0.25 }}
        >
          <JsonViewer data={contentMap[activeTab]} />
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
