package brain

import (
	"github.com/zenmodel/zenmodel"
	"github.com/zenmodel/zenmodel/brain"
	"github.com/zenmodel/zenmodel/brainlocal"
)

func New () brain.Brain{
	bp := zenmodel.NewBlueprint()

	neu1 := bp.AddNeuron(RunPythonScript)
	neu2 := bp.AddNeuron(Summarize)

	_, _ = bp.AddEntryLinkTo(neu1)
	_, _ = bp.AddLink(neu1, neu2)
	_, _ = bp.AddEndLinkFrom(neu2)

	return brainlocal.NewBrainLocal(bp)
}
