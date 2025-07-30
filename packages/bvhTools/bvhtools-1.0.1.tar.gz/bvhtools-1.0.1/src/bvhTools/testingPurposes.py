from bvhIO import readBvh, writeBvh, writeBvhToCsv, writePositionsToCsv
from bvhManipulation import centerSkeletonRoot, centerSkeletonFeet, centerSkeletonAroundJoint, rotateSkeletonWorld, rotateSkeletonLocal, centerSkeletonXZ, moveSkeleton
from bvhSlicer import getBvhSlices, groupBvhSlices, appendBvhSlices
from bvhVisualizerMpl import showBvhAnimation
if __name__ == "__main__":
    bvhData = readBvh("testBvhFiles/test.bvh")
    showBvhAnimation(bvhData)
    # bvhData.setRestPose({'LeftLeg': [ 1.31714436e-05, 90, -9.00000553e+01]})
    # writeBvh(bvhData, "testBvhFiles/testNewRest.bvh")